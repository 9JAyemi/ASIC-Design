`timescale 1ps/1ps

module tb_counter();

localparam CLK_PERIOD = 10;
localparam Bit = 4;
localparam RUNTIME = 5;

logic clk, rst, inc;
logic [Bit-1:0] mod;
logic [Bit-1:0] count;

assign mod = 4'd10;

//counter #(.Bit(Bit)) dut (.*);
counter  dut (.*);
always 
	begin 
		#(CLK_PERIOD/2) clk= ~clk; 
	end

task reset_dut();
  #(CLK_PERIOD/2) rst=1;
  @(negedge clk);
     #(CLK_PERIOD/3)  rst=0;	
endtask



initial 
	begin
      	clk=0;
	//$sdf_annotate("/home/aa2483/asap7_rundir/apr/output/counter.apr.sdf",tb_counter.dut,,"sdf_log.log","maximum");
	inc = 1'b0;
	reset_dut();
	
	#(CLK_PERIOD*10)
	inc = 1'b0;#(CLK_PERIOD);
	inc = 1'b1;#(CLK_PERIOD);
	inc = 1'b1;#(CLK_PERIOD);
	inc = 1'b0;#(CLK_PERIOD);
	inc = 1'b0;#(CLK_PERIOD);
	inc = 1'b1;#(CLK_PERIOD);
	inc = 1'b0;#(CLK_PERIOD);
	$finish;
      	end	

endmodule
