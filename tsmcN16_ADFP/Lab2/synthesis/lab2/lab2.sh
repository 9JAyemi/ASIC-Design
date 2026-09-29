#!/bin/tcsh

# load Design Compiler if this terminal hasn't already
which dc_shell >& /dev/null
if ($status != 0) then
  # ecelinux uses /usr/share/Modules; other hosts may use lowercase /usr/share/modules
  if (-e /usr/share/Modules/init/tcsh) then
    source /usr/share/Modules/init/tcsh
  else if (-e /usr/share/modules/init/tcsh) then
    source /usr/share/modules/init/tcsh
  endif
  module load synopsys/synopsys-dc
endif
which dc_shell >& /dev/null
if ($status != 0) then
  echo "dc_shell not found after module load; stopping"
  exit 1
endif

#select the values for grp between LVT16 LVT20 SVT20
set groups = (LVT16)

# only clear results for the groups being run, so other groups' reports are kept
foreach grp ($groups)
  rm -rf logs/$grp output/$grp reports/$grp
end

# edit the clock list as you like (ns)
# LVT16 search for clk_periodmin (done):
#   0.22 MET, 0.21 VIOLATED; 0.22 chosen (0.01 ns precision)
# LVT16 sweep (clk_periodmin = 0.22 ns)
# each period = multiplier x clk_periodmin
set clocks = ()
set clocks = ($clocks 0.22)     # 1.00 x 0.22 (reference)
set clocks = ($clocks 0.231)    # 1.05 x 0.22
set clocks = ($clocks 0.242)    # 1.10 x 0.22
set clocks = ($clocks 0.253)    # 1.15 x 0.22
set clocks = ($clocks 0.264)    # 1.20 x 0.22
set clocks = ($clocks 0.275)    # 1.25 x 0.22
set clocks = ($clocks 0.286)    # 1.30 x 0.22
set clocks = ($clocks 0.308)    # 1.40 x 0.22
set clocks = ($clocks 0.33)     # 1.50 x 0.22
set clocks = ($clocks 0.385)    # 1.75 x 0.22
set clocks = ($clocks 0.44)     # 2 x 0.22
set clocks = ($clocks 0.66)     # 3 x 0.22
set clocks = ($clocks 1.1)      # 5 x 0.22
set clocks = ($clocks 2.2)      # 10 x 0.22
set clocks = ($clocks 22)       # 100 x 0.22
set clocks = ($clocks 220)      # 1000 x 0.22

# LVT20 search for clk_periodmin (done):
#   coarse: 0.26 MET, 0.24 VIOLATED; fine: 0.244 MET, 0.242 VIOLATED
# LVT20 sweep (clk_periodmin = 0.244 ns)
# each period = multiplier x clk_periodmin
# set clocks = ()
# set clocks = ($clocks 0.244)    # 1.00 x 0.244 (reference)
# set clocks = ($clocks 0.2562)   # 1.05 x 0.244
# set clocks = ($clocks 0.2684)   # 1.10 x 0.244
# set clocks = ($clocks 0.2806)   # 1.15 x 0.244
# set clocks = ($clocks 0.2928)   # 1.20 x 0.244
# set clocks = ($clocks 0.305)    # 1.25 x 0.244
# set clocks = ($clocks 0.3172)   # 1.30 x 0.244
# set clocks = ($clocks 0.3416)   # 1.40 x 0.244
# set clocks = ($clocks 0.366)    # 1.50 x 0.244
# set clocks = ($clocks 0.427)    # 1.75 x 0.244
# set clocks = ($clocks 0.488)    # 2 x 0.244
# set clocks = ($clocks 0.732)    # 3 x 0.244
# set clocks = ($clocks 1.22)     # 5 x 0.244
# set clocks = ($clocks 2.44)     # 10 x 0.244
# set clocks = ($clocks 24.4)     # 100 x 0.244
# set clocks = ($clocks 244)      # 1000 x 0.244

# SVT20 sweep (clk_periodmin = 0.33 ns), kept for reference
# each period = multiplier x clk_periodmin
# set clocks = ()
# set clocks = ($clocks 0.33)     # 1.00 x 0.33 (reference)
# set clocks = ($clocks 0.3465)   # 1.05 x 0.33
# set clocks = ($clocks 0.363)    # 1.10 x 0.33
# set clocks = ($clocks 0.3795)   # 1.15 x 0.33
# set clocks = ($clocks 0.396)    # 1.20 x 0.33
# set clocks = ($clocks 0.4125)   # 1.25 x 0.33
# set clocks = ($clocks 0.429)    # 1.30 x 0.33
# set clocks = ($clocks 0.462)    # 1.40 x 0.33
# set clocks = ($clocks 0.495)    # 1.50 x 0.33
# set clocks = ($clocks 0.5775)   # 1.75 x 0.33
# set clocks = ($clocks 0.66)     # 2 x 0.33
# set clocks = ($clocks 0.99)     # 3 x 0.33
# set clocks = ($clocks 1.65)     # 5 x 0.33
# set clocks = ($clocks 3.3)      # 10 x 0.33
# set clocks = ($clocks 33)       # 100 x 0.33
# set clocks = ($clocks 330)      # 1000 x 0.33

foreach grp ($groups)
  foreach clk ($clocks)
    echo "=== $grp @ ${clk}ns ==="
    setenv CELL_GROUP $grp
    setenv CLK_PERIOD $clk
    mkdir -p logs/$grp
    mkdir -p reports/$grp
    mkdir -p output/$grp
    dc_shell -f lab2.dc.tcl -output_log_file logs/$grp/clk_${clk}ns.log
  end
end

# summary: worst slack (first path in each timing report) per clock period
# printed and saved to reports/<grp>/summary_slack.txt
foreach grp ($groups)
  set out = reports/$grp/summary_slack.txt
  echo "=== $grp worst slack per clock period (ns) ===" > $out
  foreach clk ($clocks)
    set rpt = reports/$grp/mult.${clk}.${grp}.syn_timing.rpt
    if (-e $rpt) then
      echo "$grp  clk=${clk}  `grep -m1 'slack (' $rpt`" >> $out
    else
      echo "$grp  clk=${clk}  no timing report" >> $out
    endif
  end
  echo ""
  cat $out
end

# summary: energy per cycle from the power reports
#   Switch/Int/Total are in mW, Leak is in nW (see units in the report header)
#   PDyn = Switch + Int (mW), PLeak = Leak / 1e6 (mW)
#   E = P x clk_period  -> mW x ns = pJ
# printed and saved to reports/<grp>/summary_energy.txt and reports/<grp>/energy.csv
foreach grp ($groups)
  set out = reports/$grp/summary_energy.txt
  set csv = reports/$grp/energy.csv
  echo "=== $grp energy per clock period ===" > $out
  echo "clk_ns,PDyn_mW,PLeak_mW,EDyn_pJ,ELeak_pJ,Etotal_pJ" > $csv
  printf "%-8s %10s %12s %10s %12s %10s\n" clk_ns PDyn_mW PLeak_mW EDyn_pJ ELeak_pJ Etotal_pJ >> $out
  foreach clk ($clocks)
    set rpt = reports/$grp/mult.${clk}.${grp}.syn_power.rpt
    if (-e $rpt) then
      awk -v clk=$clk -v csv=$csv '$1 == "mult" && NF >= 5 { \
        pdyn = $2 + $3; pleak = $4 / 1e6; \
        edyn = pdyn * clk; eleak = pleak * clk; \
        printf "%-8s %10.4f %12.4e %10.4f %12.4e %10.4f\n", clk, pdyn, pleak, edyn, eleak, edyn + eleak; \
        printf "%s,%g,%g,%g,%g,%g\n", clk, pdyn, pleak, edyn, eleak, edyn + eleak >> csv }' $rpt >> $out
    else
      echo "$clk  no power report" >> $out
    endif
  end
  echo ""
  cat $out
end
