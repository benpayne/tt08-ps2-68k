<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This decoder works by first deboucing the inputs to make sure that we get a clean sample of them that is syncronized to our clock.  It then looks at the down transistion of ps2_clk and reads the value of ps2_data.  It shifts this int oa 11 bit shift register.  When ps2_clk remains high for more than 1/2 of the 10kHz ps2_clk cycle it knows that the end of the data has arrived.  It then triggers a valid flag to tell the system that something has arrived.

## How to test

Simply interface a keybaord to the PS2 clock and data lines.  

## External hardware

Hook up an PS2 PMOD device to level shift the keyboards 5V to 3.3V for this chip.  