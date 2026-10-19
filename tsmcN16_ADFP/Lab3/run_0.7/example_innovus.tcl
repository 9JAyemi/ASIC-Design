
#*****************************************************************************
#	Initialization / Loading of Synthesized verilog Netlist
#*****************************************************************************


source ./var.tcl

# output folders used below; file mkdir does nothing if they already exist, so reruns work
file mkdir output cts report

### CPU setup
setDistributeHost -local 
setMultiCpuUsage -localCpu $NUM_OF_CPU

### source mmmc corner
set init_mmmc_file $mmmcFile

### set init lef
set init_lef_file $lefFile

### set ini env
set init_verilog $verilog
set init_top_cell $designName

### set ini power net
set init_pwr_net $pwrNet
set init_gnd_net $gndNet

### init design
init_design -setup scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -hold scan_hold_ffgnp_0p880v_125c_cbest_CCbest


setDesignMode -process 16

#Min-Vt & OD Jog Settings##
#setPlaceMode -place_detail_use_no_diffusion_one_site_filler true
setPlaceMode -place_detail_no_filler_without_implant true

# OD.S.17 
setPlaceMode -place_detail_check_diffusion_forbidden_spacing true

## NanoRoute  mode ##
setNanoRouteMode -drouteOnGridOnly {wire 4:7 via 3:6}
setNanoRouteMode -routeWithViaInPin {1:1}
setNanoRouteMode -routeTopRoutingLayer 9
setNanoRouteMode -routeBottomRoutingLayer 2
setNanoRouteMode -droutePostRouteSpreadWire false
setNanoRouteMode -dbViaWeight {*_P* -1}
setNanoRouteMode -routeReserveSpaceForMultiCut false
setNanoRouteMode -routeAutoPinAccessForBlockPin true
setNanoRouteMode -routeConcurrentMinimizeViaCountEffort high
setNanoRouteMode -droutePostRouteSwapVia false


### set analysis view
set_analysis_view -setup {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst scan_hold_ffgnp_0p880v_125c_cbest_CCbest} \
                  -hold {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst scan_hold_ffgnp_0p880v_125c_cbest_CCbest}



#*****************************************************************************
#	Floorplan
#*****************************************************************************



floorPlan -site core -r 1 $utilization 0 0 0 0 -noSnapToGrid



#*****************************************************************************
#	Tap / End capcells
#*****************************************************************************
### Add Boundary Cell using BWP20LVT
setEndCapMode -rightEdge        $boundaryR \
              -leftEdge         $boundaryL \
              -leftTopCorner    $boundaryLTC \
              -leftBottomCorner $boundaryLBC \
              -topEdge          $boundaryT \
              -bottomEdge       $boundaryB \
              -rightTopEdge     $boundaryLTE \
              -rightBottomEdge  $boundaryLBE \
              -fitGap true \
              -boundary_tap true

set_well_tap_mode \
   -rule 50.76 \
   -bottom_tap_cell $boundaryTapB \
   -top_tap_cell    $boundaryTapT \
   -cell            $boundaryTap

addEndCap

#verifyEndCap -report ./report/reportEndCap.rpt

### Add TapCellVPP in area to solve LUP Violation
 
addWellTap -cellInterval 50.76 -prefix WELLTAP

#verifyWellTap -report ./report/reportWellTap.rpt

### Keep the design SVT20 (BWP20P90), same as the Lab 2 synthesis (dont_use *LVT* *BWP16*).
### Set after the LVT boundary/tap cells are placed, so it only limits the cells that
### placement, CTS, hold fixing and post-route optimization can insert or swap in.
setDontUse *LVT* true
setDontUse *BWP16P90* true

connect_std_cells_to_power

saveDesign ./savedDesigns/${designName}.pre_power.enc


#*****************************************************************************
#	Power Planning 
#*****************************************************************************

sroute -connect corePin -allowJogging 0 -nets { VDD VSS } -allowLayerChange 0

addStripe -nets {VDD VSS} -layer M5 -set_to_set_distance 8 -width 0.48 -spacing 0.4 -start_x 2.96 -direction vertical -stacked_via_bottom_layer M1 -stacked_via_top_layer M5 



### Create Terminal
proc createTerminal {netName layerName} {
	set terminalRects [dbShape [dbget [dbget [dbget top.nets.name $netName -p -e].sWires.layer.extname $layerName -p2 -e].box -e] -output rect]
	foreach curTerminalRect $terminalRects {
		createPGPin $netName -net $netName -geom $layerName [lindex $curTerminalRect 0] [lindex $curTerminalRect 1] [lindex $curTerminalRect 2] [lindex $curTerminalRect 3]
	}
}
createTerminal VDD M5
createTerminal VSS M5

connect_std_cells_to_power


saveDesign ./savedDesigns/${designName}_specialRoute.enc



#timeDesign -prePlace -idealClock -expandedViews -numPaths 200 -prefix Init -outDir rpt/ini/Init.setup.timeDesign.prePlace.idealClock
#checkFPlan -outFile ./rpt/ini/Init.checkFPlan.rpt
#reportVtInstCount -detailed -outfile ./report/ini/Init.reportVtInstCount.rpt
#summaryReport -noHtml -outfile ./report/ini/Init.summaryReport.rpt


#*****************************************************************************
#	Pin Assignment
#*****************************************************************************
#odd metals routing is vertical. even metals routing is horizontal
#placement of pins

set left_ports [get_object_name [get_ports {clk rst inp_a* inp_b*}]]
set left_ports_layer [list M4]
set right_ports [get_object_name [get_ports {prod*}]]
set right_ports_layer [list M4]

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 0 -layer $left_ports_layer -offsetEnd 0.8 -offsetStart 0.8 -spreadType side -pin $left_ports -snap TRACK 
setPinAssignMode -pinEditInBatch false 

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 2 -layer $right_ports_layer -offsetEnd 0.8 -offsetStart 0.8 -spreadType side -pin $right_ports -snap TRACK 
setPinAssignMode -pinEditInBatch false 


saveDesign ./savedDesigns/${designName}.pin.enc


#*****************************************************************************
#	Placement
#*****************************************************************************


set_interactive_constraint_modes {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst scan_hold_ffgnp_0p880v_125c_cbest_CCbest}


report_clocks

create_clock -name clk  -period $clock_period -waveform [list 0 [expr $clock_period/2]] [get_ports clk]

report_clocks


setDelayCalMode -reportOutBound false
setTrialRouteMode -highEffort true -ignoreNetIsSpecial false -maxRouteLayer ${top_route_layer}
setPlaceMode -place_global_cong_effort medium
setPlaceMode -place_global_clock_gate_aware true
setOptMode -fixDrc true -fixHoldAllowOverlap true -fixFanoutLoad true -allEndPoints true -holdFixingEffort high -clkGateAware true -setupTargetSlack 0.1 -holdTargetSlack 0.05
setPlaceMode -place_detail_legalization_inst_gap 2
placeDesign
#Save_Design place
connect_std_cells_to_power
#puts "PLACE ITER 1"
#puts "Optimize timing preCTS"
optDesign -preCTS 
optDesign -preCTS -drv

connect_std_cells_to_power

saveDesign ./savedDesigns/${designName}.place.enc



#*****************************************************************************
#	CTS
#*****************************************************************************

# Setup analysis views
set_analysis_view -setup {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst} -hold {scan_hold_ffgnp_0p880v_125c_cbest_CCbest}
setAnalysisMode -analysisType onChipVariation -cppr both

# Define route types for clock tree
create_route_type -name top_rule -preferred_routing_layer_effort high -top_preferred_layer M5 -bottom_preferred_layer M5 
create_route_type -name trunk_rule -preferred_routing_layer_effort high -top_preferred_layer M5 -bottom_preferred_layer M4 
create_route_type -name leaf_rule -preferred_routing_layer_effort high -top_preferred_layer M3 -bottom_preferred_layer M2

# Specify route types for top, trunk, leaf nets
set_ccopt_property -net_type leaf  route_type leaf_rule
set_ccopt_property -net_type trunk route_type trunk_rule
set_ccopt_property -net_type top   route_type top_rule

# Configure library cells for CTS to use
set_ccopt_property buffer_cells $clockBuffers
set_ccopt_property inverter_cells $clockInvertors
set_ccopt_property use_inverters true

# Other settings
set_ccopt_property cts_add_wire_delay_in_detailed_balancer true
set_ccopt_property cts_compute_fastest_drivers_and_slews_for_clustering multi_corner
set_ccopt_property cts_clustering_net_skew_limit_as_proportion_of_skew_target 0.5
set_ccopt_property routing_top_min_fanout 2000
set_ccopt_property cell_density 0.75
set_ccopt_property adjacent_rows_legal false
set_ccopt_property ccopt_auto_limit_insertion_delay_factor 1.2
set_ccopt_property skew_band_size 0.1
set_ccopt_property useful_skew_use_gigaopt_for_mfn_chain_speed true
set_ccopt_property useful_skew_implement_using_wns_windows false
set_ccopt_property target_max_trans  100ps ;# will be ignored if set in sdc files
set_ccopt_property target_skew 30ps ;# ignored by CCOpt flow

# Create CTS specification
create_ccopt_clock_tree_spec -filename ./cts/ccopt.${clock_period}.spec
source ./cts/ccopt.${clock_period}.spec

# Set CCOpt Effort
setOptMode -usefulSkewCCOpt extreme

# Run CCopt
#ccopt_design -outDir ./cts/
clock_opt_design -outDir ./cts/
# Report timing
#timeDesign -postCTS -expandedViews -outDir ./cts/timing/

# Report clock trees to check area and other statistics
report_ccopt_clock_trees -filename ./cts/clock_trees.${clock_period}.rpt
report_ccopt_skew_groups -filename ./cts/skew_groups.${clock_period}.rpt
connect_std_cells_to_power


puts "POSTCTS ITER 0"
optDesign -postCTS 
puts "POSTCTS ITER 1"
optDesign -postCTS -drv
puts "POSTCTS ITER 2"
optDesign -postCTS -hold
connect_std_cells_to_power



saveDesign ./savedDesigns/${designName}.cts.enc



#*****************************************************************************
#	ROUTE
#*****************************************************************************

deleteRoutingHalo -allBlocks
setNanoRouteMode -routeTopRoutingLayer $top_route_layer
setNanoRouteMode -drouteFixAntenna true
setNanoRouteMode -routeInsertAntennaDiode true
setNanoRouteMode -routeAntennaCellName {ANTENNABWP30P140}
# cap detail-route repair iterations (was "default"): the M1/M2 violation count stops
# improving after ~15 iterations, and this also applies to later optDesign/ecoRoute steps
setNanoRouteMode -drouteEndIteration 15
routeDesign
setAnalysisMode -analysisType onChipVariation -cppr both
setOptMode -setupTargetSlack 0.08 -holdTargetSlack 0.04
extractRC
optDesign -postRoute
extractRC
optDesign -postRoute -drv
extractRC
optDesign -postRoute -hold
connect_std_cells_to_power


deletePlaceBlockage -all
#addDeCapCellCandidates DCAP4BWP16P90 4
#addDeCapCellCandidates DCAP8BWP16P90 8
#addDeCapCellCandidates DCAP16BWP16P90 16
#addDeCapCellCandidates DCAP32BWP16P90 32
#addDeCapCellCandidates DCAP64BWP16P90 64
                                                                            
#addDeCap -totCap 10000 -pgNet VDD -addFixAttr
addFiller -cell ${fillerCell} -prefix FILLER
connect_std_cells_to_power

ecoRoute -fix_drc
#verifyGeometry -error 10000
verifyConnectivity -error 10000
fixVia -minStep
fixVia -minCut

routeDesign -globalDetail
#verifyGeometry -error 10000
verifyConnectivity -error 10000
fixVia -minStep
fixVia -minCut
ecoRoute -fix_drc


timeDesign -postRoute -pathReports -drvReports -slackReports -numPaths 500 -prefix "${designName}.${clock_period}.postRoute.setup" -outDir timingReports
timeDesign -postRoute -hold -pathReports -slackReports -numPaths 500 -prefix "${designName}.${clock_period}.postRoute.hold" -outDir timingReports

connect_std_cells_to_power

saveDesign ./savedDesigns/${designName}.route.enc

#*****************************************************************************
#	Final
#*****************************************************************************

set stdcell_gds_files [glob /classes/ece5746/tsmcN16/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/GDS/N16ADFP_StdCell.gds]
clearDrc
verify_drc
verifyConnectivity -error 10000
verifyProcessAntenna -error 1000000

# Output GDSII
setStreamOutMode -snapToMGrid true
streamOut "./output/${designName}.${clock_period}.final.gds" -mapFile ${gdsMapFile} -libName ${designName} -structureName $designName -stripes 1 -mode ALL -merge $stdcell_gds_files -units 1000

# Output netlist
saveNetlist -excludeLeafCell -excludeCellInst $exclude_list ./output/${designName}.${clock_period}.apr.v
saveNetlist -excludeLeafCell -lineLength 10000000 -includePowerGround -includePhysicalInst -excludeCellInst $exclude_list ./output/${designName}.${clock_period}.apr.physical.v
# # Generate SDF
extractRC -outfile ./output/${designName}.${clock_period}.cap
rcOut -spef ./output/${designName}.spef 

# do_extract_model needs its view active for both setup and hold; line ~206 left only
# ss as setup and ff as hold, so both extractions failed. Activate both views, extract,
# then restore the views used for the timing reports.
set_analysis_view -setup {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst scan_hold_ffgnp_0p880v_125c_cbest_CCbest} \
                  -hold {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst scan_hold_ffgnp_0p880v_125c_cbest_CCbest}
do_extract_model -view scan_setup_ssgnp_0p720v_m40c_cworst_CCworst ./output/${designName}_slow.lib
do_extract_model -view scan_hold_ffgnp_0p880v_125c_cbest_CCbest ./output/${designName}_fast.lib
set_analysis_view -setup {scan_setup_ssgnp_0p720v_m40c_cworst_CCworst} -hold {scan_hold_ffgnp_0p880v_125c_cbest_CCbest}
write_lef_abstract "./output/${designName}.${clock_period}.lef" -stripePin -cutObsMinSpacing  -PGpinLayers {1 2 3 4 5 6 7 8 9}  -specifyTopLayer $top_route_layer
# Generate SDF
# write_sdf ./output/${designName}.${clock_period}.apr.sdf -ideal_clock_network -max_view default_setup_view -min_view default_hold_view -process best:worst -recompute_parallel_arcs
write_sdf ./output/${designName}.${clock_period}.apr.sdf -max_view scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -min_view scan_hold_ffgnp_0p880v_125c_cbest_CCbest -process best:worst -recompute_parallel_arcs

summaryReport -noHtml -outfile ./report/${designName}.summaryReport.rpt
verify_drc -report ./report/DRC.report
verifyConnectivity -report ./report/LVS.report

saveDesign ./savedDesigns/${designName}.final.enc
