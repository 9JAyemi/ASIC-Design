`timescale 1ns/1ps

module tb_fsm;

    logic bitIn;
    logic clk;
    logic reset;
    logic bitOut;

    logic [16:0] input_sequence  = 17'b00010010011001110;
    logic [16:0] expected_output  = 17'b00000010010001000;

    integer i;
    integer errors;

    myStateMachine dut (
        .bitIn(bitIn),
        .clk(clk),
        .reset(reset),
        .bitOut(bitOut)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 1'b0;
        bitIn = 1'b0;
        reset = 1'b1;
        errors = 0;

        #12;
        reset = 1'b0;

        for (i = 0; i < 17; i = i + 1) begin
            @(negedge clk);
            bitIn = input_sequence[16-i];

            @(posedge clk);
            #1;

            $display(
                "Cycle %0d: Input=%b, Output=%b, Expected=%b",
                i, bitIn, bitOut, expected_output[16-i]
            );

            if (bitOut !== expected_output[16-i]) begin
                $display("ERROR at cycle %0d", i);
                errors = errors + 1;
            end
        end

        if (errors == 0)
            $display("Pass");
        else
            $display("Fail: %0d errors", errors);

        $finish;
    end

endmodule