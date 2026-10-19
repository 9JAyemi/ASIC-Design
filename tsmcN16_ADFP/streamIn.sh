# Import the post-APR GDS of mult into Virtuoso as library 'mult_streamin'.
# Run from this directory (where Virtuoso runs and cds.lib is), after the Cadence setup:
#     source streamIn.sh
# Based on /classes/ece5746/projects/TutorialAPR/streamIn.sh; only -strmFile is changed.
# -attachTechFileOfLib tsmcN16_online needs the DEFINE tsmcN16_online line in cds.lib.
#
# Set -strmFile to the final APR GDS for clk_per_apr: Lab3/output/mult.<clk>.final.gds
# (or Lab3/run_<clk>/output/... if that run was done in a separate folder).
# If mult_streamin already exists from an earlier import, delete it in the Library
# Manager first (or change -library) so the new layout replaces it.

strmin -library 'mult_streamin'  \
-strmFile '/home/ab3394/cornell_tech/ASIC-Design/tsmcN16_ADFP/Lab3/run_0.7/output/mult.0.7.final.gds' \
-attachTechFileOfLib 'tsmcN16_online'  \
-topCell 'mult'  \
-logFile 'strmIn.log'  \
-layerMap '/classes/ece5746/tsmcN16/Executable_Package/Collaterals/Tech/iPDK/N16ADFP_iPDK/Techfile/online/1P11M_2Xa1Xd_h_3Xe_vhv_2Y2R/techfile_lib_laker/tsmcN16/tsmcN16.layermap'  \
-objectMap '/classes/ece5746/tsmcN16/Executable_Package/Collaterals/Tech/iPDK/N16ADFP_iPDK/Techfile/tsmcN16.objectmap'
