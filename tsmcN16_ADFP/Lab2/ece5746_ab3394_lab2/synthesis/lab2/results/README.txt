Lab 2 synthesis results (mult, 16-bit multiplier), saved 2026-09-22
Copied from reports/<group>/ so they survive reruns of lab2.sh.

Group   clk_period_min   Fmax
SVT20   0.33 ns          3.03 GHz  (0.327 also MET; 0.33 chosen)
LVT20   0.244 ns         4.10 GHz  (0.242 VIOLATED)

Sweep: 1x ... 1000x clk_period_min
Units: P in mW, E = P x clk_period in pJ (report Leak is nW, converted /1e6)
PDyn = Switch + Int, EDyn = PDyn x T, ELeak = PLeak x T, Etotal = EDyn + ELeak

Files per group: <group>_summary_slack.txt, <group>_summary_energy.txt, <group>_energy.csv
