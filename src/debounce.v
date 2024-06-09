
//
// This is a simple debouncer that will output the input signal after it has been stable for 128 clocks.
//

module debounce (
    input wire clk,
    input wire button,
    output wire debounced_button
);
    reg [7:0]  counter = 0;  // use high bit to flag completion
    reg        debounced_button_reg = 0;
    reg        buf_button = 0;
    reg        last_button = 0;


    always @(posedge clk) begin
        buf_button <= button;
        last_button <= buf_button;

        if (buf_button != last_button) begin
            counter <= 0;
        end else if (counter[7] == 0) begin
            counter <= counter + 1;
        end else begin
            debounced_button_reg <= last_button;
        end
    end

    assign debounced_button = debounced_button_reg;
endmodule
