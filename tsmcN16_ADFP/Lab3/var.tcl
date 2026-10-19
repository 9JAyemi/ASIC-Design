#################################### Design specific variables ##################################################################


# Lab 2 SVT20 netlist synthesized at 1.20 x clk_period_min = 1.20 x 0.33 ns = 0.396 ns (clk_per_syn)
set lab2_out "/home/ab3394/cornell_tech/ASIC-Design/tsmcN16_ADFP/Lab2/synthesis/lab2/output/SVT20"
set sdc_file "$lab2_out/mult.0.396.SVT20.syn.sdc"
set verilog "$lab2_out/mult.0.396.SVT20.syn.v"
set designName   "mult"
set top_route_layer "7"
set utilization 0.5

# APR clock period (ns). Start at clk_per_syn = 0.396; if post-route setup timing
# fails, increase this until there are no setup violations (that value = clk_per_apr).
# example_innovus.tcl redefines the clock with this period after loading the SDC.
# Run 1: 0.396 ns met setup only by overfilling the core (108.6% density, overlapping
#        cells, 211 DRC / 150 LVS errors); reports saved in report_0.396/.
# Run 2: 0.5 ns (less upsizing at the slow corner so the design fits the floorplan).
set clock_period 0.5



set pwrNet "VDD"
set gndNet "VSS"



#################################################################################################################################

set mmmcFile "./mmmcFile.tcl"

### INI Env File Setting
set NUM_OF_CPU 8


### Working Directory Setting
set ProjRoot "/classes/ece5746/tsmcN16/"



set lefFile "
    $ProjRoot/Executable_Package/Collaterals/Tech/APR/N16ADFP_APR_Innovus/N16ADFP_APR_Innovus_11M.10a.tlef
    /classes/ece5746/projects/TutorialAPR/NDR.tlef
    $ProjRoot/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/LEF/lef/N16ADFP_StdCell.lef
"




### Boundary Cell Setting
set boundaryR          "BOUNDARY_LEFTBWP20P90LVT"
set boundaryL          "BOUNDARY_RIGHTBWP20P90LVT"
set boundaryLTC        "BOUNDARY_PCORNERBWP20P90LVT"
set boundaryLBC        "BOUNDARY_NCORNERBWP20P90LVT"
set boundaryT          "BOUNDARY_PROW2BWP20P90LVT BOUNDARY_PROW3BWP20P90LVT"
set boundaryB          "BOUNDARY_NROW2BWP20P90LVT BOUNDARY_NROW3BWP20P90LVT"
set boundaryLTE        "FILL3BWP20P90LVT"
set boundaryLBE        "FILL3BWP20P90LVT"

set boundaryTapB       "BOUNDARY_NTAPBWP20P90LVT_VPP_VSS"
set boundaryTapT       "BOUNDARY_PTAPBWP20P90LVT_VPP_VSS"
set boundaryTap        "TAPCELLBWP20P90LVT_VPP_VSS"

### TapCell Setting
set tapCell {{TAPCELLBWP20P90LVT_VPP_VSS rule 50.76}}


#------------------------CTS-------------------------
### Clock Tree Cell Type
set clockInvertors "CKND16BWP16P90LVT CKND12BWP16P90LVT CKND8BWP16P90LVT CKND4BWP16P90LVT CKND2BWP16P90LVT"

set clockBuffers "CKBD1BWP16P90 CKBD1BWP16P90 CKBD2BWP16P90 CKBD2BWP16P90 CKBD4BWP16P90 CKBD4BWP16P90 CKBD8BWP16P90 CKBD8BWP16P90 CKBD12BWP16P90 CKBD12BWP16P90 CKBD16BWP16P90 CKBD16BWP16P90"

### Hold Fixing Cell Type
set holdFixCell "BUFFD1BWP20P90 BUFFD1BWP20P90LVT BUFFD2BWP20P90 BUFFD2BWP20P90LVT DEL025D1BWP20P90 DEL050D1BWP20P90 DEL075D1BWP20P90 DEL025D1BWP20P90LVT DEL050D1BWP20P90LVT DEL075D1BWP20P90LVT"

### Tie Cell Type
set tieCell "TIEHBWP20P90 TIELBWP20P90"

#----------------------POST-ROUTE--------------------
### DCAP / FILLER Cell Type
set fillerCell { FILL64BWP20P90 \
    FILL64BWP16P90 \
    FILL64BWP20P90LVT \
    FILL64BWP16P90LVT \
    FILL32BWP20P90 \
    FILL32BWP16P90 \
    FILL32BWP20P90LVT \
    FILL32BWP16P90LVT \
    FILL16BWP20P90 \
    FILL16BWP16P90 \
    FILL16BWP20P90LVT \
    FILL16BWP16P90LVT \
    FILL8BWP20P90 \
    FILL8BWP16P90 \
    FILL8BWP20P90LVT \
    FILL8BWP16P90LVT \
    FILL4BWP20P90 \
    FILL4BWP16P90 \
    FILL4BWP20P90LVT \
    FILL4BWP16P90LVT \
    FILL2BWP20P90 \
    FILL2BWP16P90 \
    FILL2BWP20P90LVT \
    FILL2BWP16P90LVT \
    FILL1BWP20P90 \
    FILL1BWP16P90 \
    FILL1BWP20P90LVT \
    FILL1BWP16P90LVT \
}

### GDS Mapping File
set gdsMapFile "$ProjRoot/Executable_Package/Collaterals/Tech/APR/N16ADFP_APR_Innovus/N16ADFP_APR_Innovus_Gdsout_11M.10a.map"


set exclude_list {BOUNDARY_LEFTBWP20P90LVT BOUNDARY_RIGHTBWP20P90LVT BOUNDARY_PCORNERBWP20P90LVT BOUNDARY_NCORNERBWP20P90LVT BOUNDARY_PROW2BWP20P90LVT BOUNDARY_PROW3BWP20P90LVT BOUNDARY_NROW2BWP20P90LVT BOUNDARY_NROW3BWP20P90LVT FILL3BWP20P90LVT FILL3BWP20P90LVT BOUNDARY_NTAPBWP20P90LVT_VPP_VSS BOUNDARY_PTAPBWP20P90LVT_VPP_VSS TAPCELLBWP20P90LVT_VPP_VSS FILL64BWP20P90  FILL64BWP16P90 FILL64BWP20P90LVT  FILL64BWP16P90LVT  FILL32BWP20P90  FILL32BWP16P90  FILL32BWP20P90LVT  FILL32BWP16P90LVT  FILL16BWP20P90  FILL16BWP16P90  FILL16BWP20P90LVT  FILL16BWP16P90LVT  FILL8BWP20P90  FILL8BWP16P90  FILL8BWP20P90LVT  FILL8BWP16P90LVT  FILL4BWP20P90  FILL4BWP16P90  FILL4BWP20P90LVT  FILL4BWP16P90LVT  FILL2BWP20P90  FILL2BWP16P90  FILL2BWP20P90LVT  FILL2BWP16P90LVT  FILL1BWP20P90  FILL1BWP16P90  FILL1BWP20P90LVT  FILL1BWP16P90LVT}

proc connect_std_cells_to_power {} {
    globalNetConnect VDD -type tiehi -inst * -verbose
    globalNetConnect VSS -type tielo -inst * -verbose
    globalNetConnect VDD -type pgpin -pin VDD* -inst * -verbose
    globalNetConnect VSS -type pgpin -pin VSS* -inst * -verbose
    globalNetConnect VDD -type pgpin -pin VPP* -inst * -verbose
    globalNetConnect VSS -type pgpin -pin VBB* -inst * -verbose
}
