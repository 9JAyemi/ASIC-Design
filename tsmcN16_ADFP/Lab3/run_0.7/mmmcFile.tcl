set ProjRoot "/classes/ece5746/tsmcN16/"
set enc_source_continue_on_error true
create_constraint_mode -name scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -sdc_files  $sdc_file
set enc_source_continue_on_error true
create_constraint_mode -name scan_hold_ffgnp_0p880v_125c_cbest_CCbest -sdc_files  $sdc_file

create_rc_corner -name cworst_m40c -T -40 -qx_tech_file $ProjRoot/Executable_Package/Collaterals/Tech/RC/N16ADFP_QRC/worst/qrcTechFile

create_rc_corner -name cbest_125c -T 125 -qx_tech_file $ProjRoot/Executable_Package/Collaterals/Tech/RC/N16ADFP_QRC/best/qrcTechFile

create_library_set -name lib_scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -timing "
    $ProjRoot/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/CCS/N16ADFP_StdCellss0p72vm40c_ccs.lib
    $ProjRoot/Executable_Package/Collaterals/IP/sram/N16ADFP_SRAM/NLDM/N16ADFP_SRAM_ss0p72v0p72vm40c_100a.lib
"

create_library_set -name lib_scan_hold_ffgnp_0p880v_125c_cbest_CCbest -timing "
    $ProjRoot/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/CCS/N16ADFP_StdCellff0p88v125c_ccs.lib
    $ProjRoot/Executable_Package/Collaterals/IP/sram/N16ADFP_SRAM/NLDM/N16ADFP_SRAM_ff0p88v0p88v125c_100a.lib
"

create_delay_corner -name scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -library_set lib_scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -rc_corner cworst_m40c

create_delay_corner -name scan_hold_ffgnp_0p880v_125c_cbest_CCbest -library_set lib_scan_hold_ffgnp_0p880v_125c_cbest_CCbest -rc_corner cbest_125c

create_analysis_view -name scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -delay_corner scan_setup_ssgnp_0p720v_m40c_cworst_CCworst -constraint_mode scan_setup_ssgnp_0p720v_m40c_cworst_CCworst
create_analysis_view -name scan_hold_ffgnp_0p880v_125c_cbest_CCbest -delay_corner scan_hold_ffgnp_0p880v_125c_cbest_CCbest -constraint_mode scan_hold_ffgnp_0p880v_125c_cbest_CCbest

