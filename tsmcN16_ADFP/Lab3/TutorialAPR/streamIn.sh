# Source this file within the PDK run directory to import a post-APR GDS
# (GDSPostAPR.gds) into Virtuoso as a design library (with the name
# 'VirtuosoDesignLibName'). 

# The number provided with the switch 'scale' indicates the factor by which
# the post-APR GDS dimensions will be multiplied by when imported into
# Virtuoso. 

# The name provided using the 'topCell' switch must correspond to the
# top-level block name in the synthesized gate level HDL netlist. 

# Supply the correct standard cell/macro library name, referenced during
# the APR, in file strminref.txt. If the referenced standard cell/macro
# library is present within the same PDK run diretory, then the top-cell
# layout in the newly created design library ('VirtuosoDesignLibName') will
# contain cells that point to the referenced standard cell/macro library.
# If this switch is excluded, then all of the macro/standard cells used
# will be created as cell views within the design library.

strmin -library 'mult_streamin'  \
-strmFile '/home/aa2483/tsmcN16_ADFP/lab2/apr/apr_clean/output/mult.2.final.gds' \
-attachTechFileOfLib 'tsmcN16_online'  \
-topCell 'mult'  \
-logFile 'strmIn.log'  \
-layerMap '/classes/ece5746/tsmcN16/Executable_Package/Collaterals/Tech/iPDK/N16ADFP_iPDK/Techfile/online/1P11M_2Xa1Xd_h_3Xe_vhv_2Y2R/techfile_lib_laker/tsmcN16/tsmcN16.layermap'  \
-objectMap '/classes/ece5746/tsmcN16/Executable_Package/Collaterals/Tech/iPDK/N16ADFP_iPDK/Techfile/tsmcN16.objectmap' 
