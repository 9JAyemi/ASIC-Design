module tb_mult;

logic [15:0] inp_a;
logic [15:0] inp_b;
logic [31:0] prod;
logic clk, rst;

mult uut (
    .inp_a(inp_a),
    .inp_b(inp_b),
    .prod(prod),
    .clk(clk),
    .rst(rst)
);

initial begin
    clk = 0;
    forever #5 clk = ~clk;
end

initial begin
    rst = 1;
    #10 rst = 0;
end

initial begin
    inp_a = 16'h0001;
    inp_b = 16'h0002;
    #20;
    inp_a = 16'h0003;
    inp_b = 16'h0004;
    #20;
    inp_a = 16'h0000;
    inp_b = 16'h0000;
    #20;
    inp_a = 16'hffff;
    inp_b = 16'hffff;
    #20;
    inp_a = 16'h00c0;
    inp_b = 16'h0acf;
    #20;
    #20;
    $finish;
end

endmodule