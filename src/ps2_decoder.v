

module ps2_decoder (
    input  wire       clk,      // clock
    input  wire       ps2_clk,  // PS2 Clock Input
    input  wire       ps2_data, // PS2 Data Input
    input  wire       reset,    // Reset signal
    output wire       valid,    // pulsed when the output data is valid
    output wire [7:0] data      // Output data
);

    localparam SYSTEM_CLOCK = 25_000_000;
    localparam PS2_CLOCK = 10_000;
    localparam [12:0] PS2_BIT_TIME = SYSTEM_CLOCK / PS2_CLOCK;

    localparam IDLE = 0, SETUP = 1, HOLD = 2, CLEAR = 3;

    reg  [10:0]  shift_reg = 0;
    reg  [12:0]  clk_timeout = 0;
    reg          reset_counter = 0;
    reg  [2:0]   state_reg = IDLE;
    reg  [7:0]   ps2_value = 0;
    reg          valid_reg = 0;

    assign data = ps2_value;
    assign valid = valid_reg;

    always @(negedge ps2_clk) begin
        shift_reg <= {shift_reg[9:0], ps2_data};
    end

    always @(posedge clk ) begin
        if (ps2_clk) begin
            if (clk_timeout == PS2_BIT_TIME) begin
                case(state_reg)
                    IDLE: begin
                        ps2_value <= {shift_reg[2], shift_reg[3], shift_reg[4], shift_reg[5], shift_reg[6], shift_reg[7], shift_reg[8], shift_reg[9]};
                        state_reg <= SETUP;
                    end
                    SETUP: begin
                        valid_reg <= shift_reg[2] ^ shift_reg[3] ^ shift_reg[4] ^ shift_reg[5] ^ shift_reg[6] ^ shift_reg[7] ^ shift_reg[8] ^ shift_reg[9] ^ shift_reg[1];
                        state_reg <= CLEAR;
                    end
                    HOLD: begin
                        state_reg <= CLEAR;
                    end
                    CLEAR: begin
                        valid_reg <= 0;
                        ps2_value <= 0;
                        clk_timeout[12] <= 1;
                    end
                endcase
            end else if (clk_timeout[12] == 0) begin
                clk_timeout <= clk_timeout + 1;
            end
        end else begin
            clk_timeout <= 0;
            state_reg <= IDLE;
        end
    end

endmodule
