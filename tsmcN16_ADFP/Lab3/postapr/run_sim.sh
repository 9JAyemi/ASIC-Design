#!/bin/bash
# Gate-level simulation of mult with the Lab 2 testbench (rtl/tb_mul.sv, unchanged).
#
#   ./run_sim.sh syn         synthesized netlist (Lab 2, SVT20, 0.396 ns) + DC SDF
#   ./run_sim.sh apr <clk>   placed-and-routed netlist <APR_DIR>/output/mult.<clk>.apr.v + Innovus SDF
#                            e.g. ./run_sim.sh apr 0.7   (default APR_DIR = Lab3/run_0.7)
#   APR_DIR=../run_0.8 ./run_sim.sh apr 0.8              (another APR run folder)
#
# Opens QuestaSim with the waveform from Lab 2's wave.do and runs the testbench.
# The SDF is annotated onto the testbench's instance /tb_mult/uut (max = worst-case delays).
# Add -c as a last argument to run in the terminal without the GUI.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"                     # .../tsmcN16_ADFP
STDCELL=/classes/ece5746/tsmcN16/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/VERILOG/N16ADFP_StdCell.v
TB="$ROOT/Lab2/rtl/tb_mul.sv"
WAVE="$ROOT/Lab2/wave.do"
SYN_DIR="$ROOT/Lab2/synthesis/lab2/output/SVT20"
APR_DIR="${APR_DIR:-$ROOT/Lab3/run_0.7}"   # final APR run (clk_per_apr = 0.7 ns)

mode="$1"
case "$mode" in
  syn)
    NETLIST="$SYN_DIR/mult.0.396.SVT20.syn.v"
    SDF="$SYN_DIR/mult.0.396.syn.sdf"
    shift ;;
  apr)
    clk="$2"
    [ -n "$clk" ] || { echo "usage: $0 apr <clk_period>   (e.g. 0.6)"; exit 1; }
    NETLIST="$APR_DIR/output/mult.$clk.apr.v"
    SDF="$APR_DIR/output/mult.$clk.apr.sdf"
    shift 2 ;;
  *)
    sed -n '2,12p' "$0"; exit 1 ;;
esac
GUI="-gui"; [ "$1" = "-c" ] && GUI="-c"

for f in "$STDCELL" "$NETLIST" "$SDF" "$TB"; do
  [ -f "$f" ] || { echo "missing: $f"; exit 1; }
done

module load siemens/questasim 2>/dev/null || true
cd "$HERE"
LIB="work_$mode${clk:+_$clk}"
# reuse the library if it exists (vlog recompiles every module into it); deleting it fails
# while an earlier QuestaSim window for the same mode is still open
[ -d "$LIB" ] || vlib "$LIB" >/dev/null
# -timescale gives the testbench (which has none) the same 1ns/1ps as the cell models
vlog -work "$LIB" -sv -timescale 1ns/1ps "$STDCELL" "$NETLIST" "$TB"

echo "netlist: $NETLIST"
echo "sdf:     $SDF (max delays on /tb_mult/uut)"
DO="run -all; quit -f"
[ "$GUI" = "-gui" ] && [ -f "$WAVE" ] && DO="do $WAVE; run -all; wave zoom full"
vsim $GUI -L "$LIB" -lib "$LIB" tb_mult \
     -sdfmax /tb_mult/uut="$SDF" +sdf_verbose \
     -voptargs=+acc -l "sim_$mode${clk:+_$clk}.log" -do "$DO"
