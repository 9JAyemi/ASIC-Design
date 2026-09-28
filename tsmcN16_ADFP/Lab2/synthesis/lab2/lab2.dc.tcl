# disclaimer: All the values given here are just for illustrative purpose
# Change all the path according to your run directory
# Please go through the file before sourcing it
# Try to run all the command one by one at least for the first time



# Initial setup
set_host_options -max_cores 8
set_units -time ns
source -continue_on_error ./suppress_message.tcl


# tsmcN16 lib
set search_path [list "/classes/ece5746/tsmcN16/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/NLDM/" ]
set link_library "* N16ADFP_StdCelltt0p8v25c.db"
set target_library "N16ADFP_StdCelltt0p8v25c.db"


# ################################# DESIGN SPECIFIC ###################################################
# TOP_LEVEL_NAME
set top_level 			"mult"
# PATH TO YOUR VERILOG NETLIST
set netlist_search_path "../../rtl"
# NETLIST NAME > list of RTL files in design. 
set netlist_name "mul.sv"
# verilog format <verilog|sverilog|vhdl>
set file_type "sverilog"

# ################################################################################################

# CLOCK PERIOD
set clk_period 			$::env(CLK_PERIOD)


# Read verilog files
#analyze -format $file_type $netlist_search_path/$netlist_name

foreach i $netlist_name {
analyze -format $file_type $netlist_search_path/$i
}


elaborate $top_level
list_designs
current_design $top_level



if {![info exists ::env(CELL_GROUP)]} {
    puts "CELL_GROUP not set"; exit 1
}

set grp $::env(CELL_GROUP)

switch -- $grp {
    LVT16 { set_target_library_subset -use [list *BWP16*LVT]}
    LVT20 { set_target_library_subset -use [list *BWP20*LVT]}
    SVT20 { set_target_library_subset -dont_use [list *LVT* *BWP16*] }
    default { puts "Bad CELL_GROUP: $grp"; exit 1 }
}



#Create real clock if clock port is found
if {[sizeof_collection [get_ports clk]] > 0} {
  set clk_name "clk"
  set clk_port "clk"
  #If no waveform is specified, 50% duty cycle is assumed
  create_clock -name $clk_name -period $clk_period [get_ports $clk_port] 
  set_drive 0 [get_clocks $clk_name] 
}

set_clock_uncertainty 0.01 [get_clocks $clk_name]
set_clock_transition 0.1 [get_clocks $clk_name]

set_wire_load_mode "segmented" 

set typical_input_delay 0.010
set typical_output_delay 0.010
set typical_wire_load 0.010 

# Set maximum fanout of gates
set_max_fanout 16 $top_level 

# Configure the clock network
set_fix_hold [all_clocks] 
set_dont_touch_network $clk_port 

set_driving_cell -lib_cell INVD1BWP20P90 [all_inputs]
set_input_delay $typical_input_delay [all_inputs] -clock $clk_name 
remove_input_delay -clock $clk_name [find port $clk_port]
set_output_delay $typical_output_delay [all_outputs] -clock $clk_name 

# Set loading of outputs 
set_load $typical_wire_load [all_outputs] 

# Verify the design
check_design

# Synthesize the design
compile_ultra




# Generate structural verilog netlist
write_file -hierarchy -format verilog -output "./output/${grp}/${top_level}.${clk_period}.${grp}.syn.v"
# Save current design
#write_file -hierarchy -format ddc -output "./output/${top_level}.${clk_period}.${grp}.ddc"

# Generate Standard Delay Format (SDF) file
write_sdf -context verilog "./output/${grp}/${top_level}.${clk_period}.syn.sdf"

# Generate timing constraints file
write_sdc "./output/${grp}/${top_level}.${clk_period}.${grp}.syn.sdc"

# Generate report file
set maxpaths 100
#set minpaths 100
set rpt_file "./reports/${grp}/${top_level}.${clk_period}.${grp}.syn"

check_design > ${rpt_file}.rpt
report_area -hierarchy -designware >> ${rpt_file}_area.rpt
report_power -hier -analysis_effort medium >> ${rpt_file}_power.rpt
report_design >> ${rpt_file}.rpt
report_cell >> ${rpt_file}.rpt
report_port -verbose >> ${rpt_file}.rpt
report_compile_options >> ${rpt_file}.rpt
report_constraint -all_violators -verbose >> ${rpt_file}_violaters.rpt
report_timing -path full -delay max -max_paths $maxpaths -nworst 100 >> ${rpt_file}_timing.rpt

# Exit dc_shell
quit
