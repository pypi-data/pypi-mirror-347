from amaranth import *
from amaranth.utils import *
import amaranth.lib.memory as memory
from amaranth.hdl import AlreadyElaborated

from typing import Optional, Any, final
from collections.abc import Iterable

from transactron.utils.amaranth_ext.elaboratables import OneHotMux

from .. import get_src_loc
from amaranth_types.types import ShapeLike, ValueLike

__all__ = ["MultiReadMemory", "MultiportXORMemory", "MultiportILVTMemory"]


@final
class MultipleWritePorts(Exception):
    """Exception raised when a single write memory is being requested multiple write ports."""


class ReadPort:

    def __init__(
        self,
        memory: "BaseMultiportMemory",
        transparent_for: Iterable[Any] = (),
        src_loc=0,
    ):
        self.src_loc = get_src_loc(src_loc)
        self.transparent_for = transparent_for
        self.en = Signal()
        self.addr = Signal(range(memory.depth))
        self.data = Signal(memory.shape)
        self._memory = memory
        memory.read_ports.append(self)


class WritePort:

    def __init__(
        self,
        memory: "BaseMultiportMemory",
        granularity: Optional[int] = None,
        src_loc=0,
    ):
        self.src_loc = get_src_loc(src_loc)

        shape = memory.shape
        if granularity is None:
            en_width = 1
        elif not isinstance(granularity, int) or granularity <= 0:
            raise TypeError(f"Granularity must be a positive integer or None, " f"not {granularity!r}")
        elif shape.signed:
            raise ValueError("Granularity cannot be specified for a memory with a signed shape")
        elif shape.width % granularity != 0:
            raise ValueError("Granularity must evenly divide data width")
        else:
            en_width = shape.width // granularity

        self.en = Signal(en_width)
        self.addr = Signal(range(memory.depth))
        self.data = Signal(shape)
        self.granularity = granularity
        self._memory = memory
        memory.write_ports.append(self)


class BaseMultiportMemory(Elaboratable):
    def __init__(
        self,
        *,
        shape: ShapeLike,
        depth: int,
        init: Iterable[ValueLike],
        attrs: Optional[dict[str, str]] = None,
        src_loc_at: int = 0,
    ):
        """
        Parameters
        ----------
        shape: ShapeLike
            Shape of each memory row.
        depth : int
            Number of memory rows.
        init : iterable of initial values
            Initial values for memory rows.
        src_loc: int
            How many stack frames deep the source location is taken from.
        """

        self.shape = Shape.cast(shape)
        self.depth = depth
        self.init = init
        self.attrs = attrs
        self.src_loc = src_loc_at

        self.read_ports: "list[ReadPort]" = []
        self.write_ports: "list[WritePort]" = []
        self._frozen = False

    def read_port(self, *, domain: str = "sync", transparent_for: Iterable[Any] = (), src_loc_at: int = 0):
        if self._frozen:
            raise AlreadyElaborated("Cannot add a memory port to a memory that has already been elaborated")
        if domain != "sync":
            raise ValueError("Invalid port domain: Only synchronous memory ports supported.")
        return ReadPort(
            memory=self,
            transparent_for=transparent_for,
            src_loc=1 + src_loc_at,
        )

    def write_port(self, *, domain: str = "sync", granularity: Optional[int] = None, src_loc_at: int = 0):
        if self._frozen:
            raise AlreadyElaborated("Cannot add a memory port to a memory that has already been elaborated")
        if domain != "sync":
            raise ValueError("Invalid port domain: Only synchronous memory ports supported.")
        return WritePort(
            memory=self,
            granularity=granularity,
            src_loc=1 + src_loc_at,
        )


class MultiReadMemory(BaseMultiportMemory):
    """Memory with one write and multiple read ports.

    One can request multiple read ports and not more than 1 write port. Module internally
    uses multiple (number of read ports) instances of amaranth.lib.memory.Memory with one
    read and one write port.

    """

    def write_port(self, *, domain: str = "sync", granularity: Optional[int] = None, src_loc_at: int = 0):
        if self.write_ports:
            raise MultipleWritePorts("Cannot add multiple write ports to a single write memory")
        return super().write_port(domain=domain, granularity=granularity, src_loc_at=src_loc_at)

    def elaborate(self, platform):
        m = Module()

        self._frozen = True

        write_port = self.write_ports[0] if self.write_ports else None
        for port in self.read_ports:
            # for each read port a new single port memory block is generated
            mem = memory.Memory(
                shape=self.shape, depth=self.depth, init=self.init, attrs=self.attrs, src_loc_at=self.src_loc
            )
            m.submodules += mem
            physical_write_port = mem.write_port(granularity=write_port.granularity) if write_port else None
            physical_read_port = mem.read_port(
                transparent_for=(
                    [physical_write_port] if physical_write_port and write_port in port.transparent_for else []
                )
            )
            m.d.comb += [
                physical_read_port.addr.eq(port.addr),
                port.data.eq(physical_read_port.data),
                physical_read_port.en.eq(port.en),
            ]

            if physical_write_port and write_port:
                m.d.comb += [
                    physical_write_port.addr.eq(write_port.addr),
                    physical_write_port.data.eq(write_port.data),
                    physical_write_port.en.eq(write_port.en),
                ]

        return m


class MultiportXORMemory(BaseMultiportMemory):
    """Multiport memory based on xor.

    Multiple read and write ports can be requested. Memory is built of
    (number of write ports) * (number of write ports - 1 + number of read ports) single port
    memory blocks. XOR is used to enable writing multiple values in one cycle and reading correct values.
    Writing two different values to the same memory address in one cycle has undefined behavior.
    Write port granularity is not yet supported.

    """

    def write_port(self, *, domain: str = "sync", granularity: Optional[int] = None, src_loc_at: int = 0):
        if granularity is not None:
            raise ValueError("Granularity is not supported.")
        return super().write_port(domain=domain, granularity=granularity, src_loc_at=src_loc_at)

    def elaborate(self, platform):
        m = Module()

        self._frozen = True

        write_xors = [Value.cast(0) for _ in self.write_ports]
        read_xors = [Value.cast(0) for _ in self.read_ports]

        write_regs_addr = [Signal(range(self.depth)) for _ in self.write_ports]
        write_regs_data = [Signal(self.shape) for _ in self.write_ports]
        read_en_bypass = [Signal() for _ in self.read_ports]

        for index, write_port in enumerate(self.write_ports):
            m.d.sync += [write_regs_data[index].eq(write_port.data), write_regs_addr[index].eq(write_port.addr)]
            write_xors[index] ^= write_regs_data[index]
            for i in range(len(self.write_ports) - 1):
                mem = memory.Memory(
                    shape=self.shape, depth=self.depth, init=[], attrs=self.attrs, src_loc_at=self.src_loc
                )
                mem_name = f"memory_{index}_{i}"
                m.submodules[mem_name] = mem
                physical_write_port = mem.write_port()
                physical_read_port = mem.read_port(transparent_for=[physical_write_port])

                idx = i + 1 if i >= index else i
                write_xors[idx] ^= physical_read_port.data

                m.d.comb += [physical_read_port.en.eq(1), physical_read_port.addr.eq(self.write_ports[idx].addr)]

                m.d.sync += [
                    physical_write_port.en.eq(write_port.en),
                    physical_write_port.addr.eq(write_port.addr),
                ]

        for index, write_port in enumerate(self.write_ports):
            write_xor = Signal(self.shape)
            m.d.comb += [write_xor.eq(write_xors[index])]

            for i in range(len(self.write_ports) - 1):
                mem_name = f"memory_{index}_{i}"
                mem = m.submodules[mem_name]
                physical_write_port = mem.write_ports[0]

                m.d.comb += [physical_write_port.data.eq(write_xor)]

            init = self.init if index == 0 else []
            read_block = MultiReadMemory(
                shape=self.shape, depth=self.depth, init=init, attrs=self.attrs, src_loc_at=self.src_loc
            )
            mem_name = f"read_block_{index}"
            m.submodules[mem_name] = read_block
            r_write_port = read_block.write_port()
            r_read_ports = [read_block.read_port() for _ in self.read_ports]
            m.d.comb += [r_write_port.data.eq(write_xor)]

            m.d.sync += [r_write_port.addr.eq(write_port.addr), r_write_port.en.eq(write_port.en)]

            write_addr_bypass = Signal(range(self.depth))
            write_data_bypass = Signal(self.shape)
            write_en_bypass = Signal()
            m.d.sync += [
                write_addr_bypass.eq(write_regs_addr[index]),
                write_data_bypass.eq(write_xor),
                write_en_bypass.eq(r_write_port.en),
            ]

            for idx, port in enumerate(r_read_ports):
                read_addr_bypass = Signal(range(self.depth))

                m.d.sync += [
                    read_addr_bypass.eq(self.read_ports[idx].addr),
                    read_en_bypass[idx].eq(self.read_ports[idx].en),
                ]

                single_stage_bypass = Mux(
                    (read_addr_bypass == write_addr_bypass) & read_en_bypass[idx] & write_en_bypass,
                    write_data_bypass,
                    port.data,
                )

                if write_port in self.read_ports[idx].transparent_for:
                    read_xors[idx] ^= Mux(
                        (read_addr_bypass == write_regs_addr[index]) & r_write_port.en,
                        write_xor,
                        single_stage_bypass,
                    )
                else:
                    read_xors[idx] ^= single_stage_bypass

                m.d.comb += [port.addr.eq(self.read_ports[idx].addr), port.en.eq(self.read_ports[idx].en)]

        for index, port in enumerate(self.read_ports):
            sync_data = Signal.like(port.data)
            m.d.sync += sync_data.eq(port.data)
            m.d.comb += [port.data.eq(Mux(read_en_bypass[index], read_xors[index], sync_data))]

        return m


class MultiportILVTMemory(BaseMultiportMemory):
    """Multiport memory based on Invalidation Live Value Table.

    Multiple read and write ports can be requested. Memory is built of
    number of write ports memory blocks with multiple read and multi-ported Invalidation Live Value Table.
    ILVT is a XOR based memory that returns the number of the memory bank in which the current value is stored.
    Width of data stored in ILVT is the binary logarithm of the number of write ports.
    Writing two different values to the same memory address in one cycle has undefined behavior.

    """

    def elaborate(self, platform):
        m = Module()

        self._frozen = True

        m.submodules.ilvt = ilvt = MultiportXORMemory(
            shape=bits_for(len(self.write_ports) - 1), depth=self.depth, init=self.init, src_loc_at=self.src_loc + 1
        )

        ilvt_write_ports = [ilvt.write_port() for _ in self.write_ports]
        ilvt_read_ports = [ilvt.read_port() for _ in self.read_ports]

        write_addr_bypass = [Signal(port.addr.shape()) for port in self.write_ports]
        write_data_bypass = [Signal(self.shape) for _ in self.write_ports]
        write_en_bypass = [Signal(port.en.shape()) for port in self.write_ports]

        m.d.sync += [write_addr_bypass[index].eq(port.addr) for index, port in enumerate(self.write_ports)]
        m.d.sync += [write_data_bypass[index].eq(port.data) for index, port in enumerate(self.write_ports)]
        m.d.sync += [write_en_bypass[index].eq(port.en) for index, port in enumerate(self.write_ports)]

        for index, write_port in enumerate(ilvt_write_ports):
            # address a is marked as last changed in bank k (k gets stored at a in ILVT)
            # when any part of value at address a gets overwritten by port k
            m.d.comb += [
                write_port.addr.eq(self.write_ports[index].addr),
                write_port.en.eq(self.write_ports[index].en.any()),
                write_port.data.eq(index),
            ]

            mem = MultiReadMemory(
                shape=self.shape, depth=self.depth, init=self.init, attrs=self.attrs, src_loc_at=self.src_loc
            )
            mem_name = f"bank_{index}"
            m.submodules[mem_name] = mem
            bank_write_port = mem.write_port(granularity=self.write_ports[index].granularity)
            bank_read_ports = [mem.read_port() for _ in self.read_ports]

            m.d.comb += [
                bank_write_port.addr.eq(self.write_ports[index].addr),
                bank_write_port.en.eq(self.write_ports[index].en),
                bank_write_port.data.eq(self.write_ports[index].data),
            ]
            for idx, port in enumerate(bank_read_ports):
                m.d.comb += [
                    port.en.eq(self.read_ports[idx].en),
                    port.addr.eq(self.read_ports[idx].addr),
                ]

        for index, read_port in enumerate(self.read_ports):
            m.d.comb += [ilvt_read_ports[index].addr.eq(read_port.addr), ilvt_read_ports[index].en.eq(read_port.en)]

            read_en_bypass = Signal()
            read_addr_bypass = Signal(self.shape)

            m.d.sync += [read_en_bypass.eq(read_port.en), read_addr_bypass.eq(read_port.addr)]

            bank_data = Signal(self.shape)
            with m.Switch(ilvt_read_ports[index].data):
                for value in range(len(self.write_ports)):
                    with m.Case(value):
                        m.d.comb += [bank_data.eq(m.submodules[f"bank_{value}"].read_ports[index].data)]

            mux_inputs = [
                ((write_addr_bypass[idx] == read_addr_bypass) & write_en_bypass[idx], write_data_bypass[idx])
                for idx, write_port in enumerate(self.write_ports)
                if write_port in read_port.transparent_for
            ]
            new_data = OneHotMux.create(m, mux_inputs, bank_data)

            sync_data = Signal.like(read_port.data)
            m.d.sync += sync_data.eq(read_port.data)
            m.d.comb += [read_port.data.eq(Mux(read_en_bypass, new_data, sync_data))]

        return m
