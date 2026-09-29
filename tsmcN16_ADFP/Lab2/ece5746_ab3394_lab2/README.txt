ECE 5746 Lab 2 - ab3394
16-bit registered multiplier: RTL, testbench, synthesis sweeps (SVT20, LVT20, LVT16)

ece5746_ab3394_lab2_report.pdf   the report

rtl/
  mul.sv                 design (module mult)
  tb_mul.sv              testbench (module tb_mult)
  wave.do                QuestaSim waveform setup

synthesis/lab2/
  lab2.dc.tcl            Design Compiler script (reads CELL_GROUP and CLK_PERIOD)
  suppress_message.tcl   sourced by lab2.dc.tcl
  lab2.sh                runs the clock-period sweep for the groups in `groups`,
                         then writes slack and energy summaries (run: ./lab2.sh)
  plot_energy.py         energy vs frequency plots          (python3.12 plot_energy.py)
  ppa_report.py          area/drive/fan-in/path statistics  (python3.12 ppa_report.py)
  lab2_report.py         builds the LaTeX report and PDF    (python3.12 lab2_report.py)
  check_sources.py       maps every number in the report to its line in the DC reports
  reports/<group>/       DC reports per clock period: mult.<clk>.<group>.syn{,_area,_timing,_power,_violaters}.rpt,
                         plus summary_slack.txt, summary_energy.txt, energy.csv
  results/               summaries, per-point PPA tables (ppa_<group>.csv), Excel workbook
  plots/                 figures used in the report

clk_period_min: SVT20 0.33 ns (3030 MHz), LVT20 0.244 ns (4098 MHz), LVT16 0.22 ns (4545 MHz)
Energy: E = P x clk_period; Switch/Int power in mW, Leak in nW (converted to mW); mW x ns = pJ
Netlists (output/) and DC logs are not included; lab2.sh regenerates them.
