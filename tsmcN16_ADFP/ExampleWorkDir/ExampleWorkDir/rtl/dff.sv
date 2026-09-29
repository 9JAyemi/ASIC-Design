module dff #(parameter Bit = 1) (input logic [Bit-1:0]d,
				input logic clk, rst,en,
				output logic [Bit-1:0]q);

always_ff @(posedge clk) begin
priority case(1'b1) 
rst: q<='b0;
//en: q<=d;
default: begin if(en) begin
		q<=d;
		end
	end
endcase
end

endmodule
 