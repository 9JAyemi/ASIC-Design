module mult ( input logic [15:0] inp_a,
input logic [15:0] inp_b,
output logic [31:0] prod,
input logic clk, rst);

always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
        prod <= 32'b0;
    end else begin
        prod <= inp_a * inp_b;
    end
end
endmodule