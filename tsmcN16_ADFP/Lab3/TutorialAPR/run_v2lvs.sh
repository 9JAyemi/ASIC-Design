# path to your post apr verilog netlist. 
set DesignPhysical = "./output/mult.2.apr.physical.v"
# output directory where you want to generate your .sp file
set outputDirectory = "./output"
# name of your output .sp file 
set outputSpice = "mult.sp"
# path to standard cell spice netlist. Dont change this. 
set StandardCellSpiceNetlist = "/classes/ece5746/tsmcN16/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/SPICE/N16ADFP_StdCell_100b.spi"

v2lvs -i -v $DesignPhysical -o $outputDirectory/$outputSpice -n -a [] -lsr $StandardCellSpiceNetlist -s $StandardCellSpiceNetlist
