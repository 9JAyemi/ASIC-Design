module counter #(parameter Bit =4) (input logic clk, rst, inc,
				input logic [Bit-1:0] mod,
				output logic[Bit-1:0] count);

logic [Bit-1:0] count_next;

logic up;
assign up = (count == mod);



always_comb begin

case({inc,up})
2'b10: count_next=count+1;
2'b11: count_next='b0;
default: count_next = count;
endcase
end

dff #(.Bit(Bit)) dff_count(.clk(clk), .rst(rst), .d(count_next), .q(count),.en(inc));
endmodule
