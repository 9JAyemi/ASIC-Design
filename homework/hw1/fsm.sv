module myStateMachine
(
    input  logic bitIn,
    input  logic clk,
    input  logic reset,
    output logic bitOut
);

typedef enum logic [2:0] {
    S0 = 3'd0,  // No matching prefix
    S1 = 3'd1,  // Matched 1
    S2 = 3'd2,  // Matched 10
    S3 = 3'd3,  // Matched 100
    S4 = 3'd4   // Matched 1001
} state_t;

state_t currentState, nextState;

always_comb begin
    nextState = S0;
    bitOut = 1'b0;

    case (currentState)
        S0: begin
            nextState = state_t'(bitIn ? S1 : S0);
        end

        S1: begin
            nextState = state_t'(bitIn ? S1 : S2);
        end

        S2: begin
            nextState = state_t'(bitIn ? S1 : S3);
        end

        S3: begin
            nextState = state_t'(bitIn ? S4 : S0);
        end

        S4: begin
            bitOut = 1'b1;
            nextState = state_t'(bitIn ? S1 : S2);
        end

        default: begin
            nextState = S0;
            bitOut = 1'b0;
        end
    endcase
end

always_ff @(posedge clk or posedge reset) begin
    if (reset)
        currentState <= S0;
    else
        currentState <= nextState;
end

endmodule