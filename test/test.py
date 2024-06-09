# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Edge, First
from cocotb.clock import Clock, Timer

async def send_bit(ps2_clk, ps2_data, bit):
    ps2_data.value = bit
    ps2_clk.value = 1
    await Timer(50, units="us")
    ps2_clk.value = 0
    await Timer(50, units="us")


async def send_bits(ps2_clk, ps2_data, value, bit_count=8, parity_valid=True, stop_valid=True):
    await send_bit(ps2_clk, ps2_data, 0)  # start bit
    parity = 0
    for i in range(bit_count):
        bit = (value >> (i)) & 1
        parity ^= bit
        await send_bit(ps2_clk, ps2_data, bit)
    if parity_valid:
        await send_bit(ps2_clk, ps2_data, not parity)
    else:
        await send_bit(ps2_clk, ps2_data, parity)
    if stop_valid:
        await send_bit(ps2_clk, ps2_data, 1)  # stop bit
    ps2_clk.value = 1

@cocotb.test()
async def ps2_decode_test(dut):
    """Test getting one byte from keyboard."""

    dut.rst_n.value = 0
    await Timer(1, units="us")
    dut.rst_n.value = 1

    #cocotb.start_saving_waves()
    cocotb.start_soon(Clock(dut.clk, 40, units="ns").start())

    dut.ps2_clk.value = 1
    dut.ps2_data.value = 1
    
    await Timer(1, units="us")

    cocotb.start_soon(send_bits(dut.ps2_clk, dut.ps2_data, 0xC2))

    # wait for rising edge of valid and check data
    await RisingEdge(dut.valid)
    assert dut.uo_out == 0xC2, f"Expected 0xC2, got {dut.uo_out.value.hex()}"
    await Timer(50, units="ns")

    # wait enough time for the valid signal to go low and validate
    assert dut.valid == 0, "Valid not cleared properly"
    assert dut.uio_oe == 0x01, f"Expected 0xFF, got {dut.uio_oe.value.hex()}"

    await Timer(100, units="us")


@cocotb.test()
async def ps2_decode_second_test(dut):
    """Test another byte."""

    #cocotb.start_saving_waves()
    cocotb.start_soon(Clock(dut.clk, 40, units="ns").start())

    dut.ps2_clk.value = 1
    dut.ps2_data.value = 1

    await Timer(1, units="us")

    cocotb.start_soon(send_bits(dut.ps2_clk, dut.ps2_data, 0xF0))

    # wait for rising edge of valid and check data
    await RisingEdge(dut.valid)
    assert dut.uo_out == 0xF0, f"Expected 0xF0, got {dut.uo_out.value.hex()}"

    # wait enough time for the valid signal to go low and validate
    await Timer(50, units="ns")
    assert dut.valid == 0, "Valid not cleared properly"
    assert dut.uio_oe == 0x01, f"Expected 0xFF, got {dut.uio_oe.value.hex()}"

    await Timer(100, units="us")

@cocotb.test()
async def ps2_decode_partial_test(dut):
    """Test the a failed transmit."""

    #cocotb.start_saving_waves()
    cocotb.start_soon(Clock(dut.clk, 40, units="ns").start())

    dut.ps2_clk.value = 1
    dut.ps2_data.value = 1

    await Timer(1, units="us")

    cocotb.start_soon(send_bits(dut.ps2_clk, dut.ps2_data, 0xF0, bit_count=5, parity_valid=False, stop_valid=False))

    # wait for rising edge of valid and check data
    to = Timer(1.5, units='ms')
    res = await First(RisingEdge(dut.valid), to)

    print(f"res: {res}")

    assert isinstance(res, Timer) , "Expected timeout got rising edge"

async def send_two_bytes(ps2_clk, ps2_data, value1, value2):
    await send_bits(ps2_clk, ps2_data, value1)
    await Timer(100, units="us")
    await send_bits(ps2_clk, ps2_data, value2)

@cocotb.test()
async def ps2_decode_two_bytes_test(dut):
    """Test receiveing two keycodes."""

    #cocotb.start_saving_waves()
    cocotb.start_soon(Clock(dut.clk, 40, units="ns").start())

    dut.ps2_clk.value = 1
    dut.ps2_data.value = 1

    await Timer(1, units="us")

    cocotb.start_soon(send_two_bytes(dut.ps2_clk, dut.ps2_data, 0xF0, 0x15))

    # wait for rising edge of valid and check data
    await RisingEdge(dut.valid)
    assert dut.uo_out == 0xF0, f"Expected 0xF0, got {dut.uo_out.value.hex()}"

    # wait enough time for the valid signal to go low and validate
    await Timer(50, units="ns")
    assert dut.valid == 0, "Valid not cleared properly"
    assert dut.uio_oe == 0x01, f"Expected 0xFF, got {dut.uio_oe.value.hex()}"

    # wait for rising edge of valid and check data
    await RisingEdge(dut.valid)
    assert dut.uo_out == 0x15, f"Expected 0xF0, got {dut.uo_out.value.hex()}"

    # wait enough time for the valid signal to go low and validate
    await Timer(50, units="ns")
    assert dut.valid == 0, "Valid not cleared properly"
    assert dut.uio_oe == 0x01, f"Expected 0xFF, got {dut.uio_oe.value.hex()}"

    await Timer(100, units="us")
