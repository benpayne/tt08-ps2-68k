/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_benpayne_ps2_decoder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out[7:2] = 6'b0;  // Example: uio_out[7:1] are always 0
  assign uio_oe = 8'b11;  // Example: All pins are outputs

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, 1'b0};

  wire ps2_clk_internal;
  wire ps2_data_internal;
  
  debounce ps2_clk_debounce(
    .clk(clk),
    .reset(~rst_n),
    .button(ui_in[0]),
    .debounced_button(ps2_clk_internal)
  );

  debounce ps2_data_debounce(
    .clk(clk),
    .reset(~rst_n),
    .button(ui_in[1]),
    .debounced_button(ps2_data_internal)
  );

  ps2_decoder ps2_decoder_inst (
    .clk(clk),
    .reset(~rst_n),
    .ps2_clk(ps2_clk_internal),
    .ps2_data(ps2_data_internal),
    .data(uo_out),
    .valid(uio_out[0]),
    .interupt(uio_out[1]),
    .int_clear(ui_in[2])
  );
endmodule
