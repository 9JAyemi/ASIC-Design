# Report cross-check sheet

Each value below is what `lab2_report.py` puts in the report. Links go to the line in the DC report it was read from (Ctrl+click in the editor, or open the Markdown preview). Area in um^2.

## SVT20

- F_max point: 0.33 ns; slowest point: 330 ns
- First positive slack: 1.65 ns
- Minimum E_total: 0.5226 pJ at 3.3 ns (check against `reports/SVT20/energy.csv`)

### SVT20 @ 0.33 ns (1x, 3030.3 MHz) - F_max (Performance / Drive strength / critical-path list); netlist table row

**syn_area.rpt**

- Number of cells = **1148** -> [mult.0.33.SVT20.syn_area.rpt:15](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.33.SVT20.syn_area.rpt:17](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **208** -> [mult.0.33.SVT20.syn_area.rpt:19](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **44.58** -> [mult.0.33.SVT20.syn_area.rpt:23](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.33.SVT20.syn_area.rpt:24](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L24)
- Total cell area = **525.71** -> [mult.0.33.SVT20.syn_area.rpt:28](../reports/SVT20/mult.0.33.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[5]** -> [mult.0.33.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[29]** -> [mult.0.33.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L17)
- Path cells = **15** (cell lines between [Point:26](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L26) and [data arrival:48](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L48), not counting the endpoint flop's D pin)
- Data arrival = **0.31 ns** -> [mult.0.33.SVT20.syn_timing.rpt:48](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L48)
- Slack = **0.00 ns** -> [mult.0.33.SVT20.syn_timing.rpt:60](../reports/SVT20/mult.0.33.SVT20.syn_timing.rpt#L60)
- Path cells (function x drive), avg drive x2.6: `XOR2x2 CKNx8 CKBx1 OAI22x1 FA1x1 XOR3x4 OAI21x2 IOA21x1 NR2x4 NR2x4 CKND2x4 INVx4 ND2x1 IAOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.913 mW**, Int = **1.883 mW**, Leak = **1070 nW** -> [mult.0.33.SVT20.syn_power.rpt:41](../reports/SVT20/mult.0.33.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.33 = **0.9227 pJ**, E_leak = Leak/1e6 x 0.33 = **3.531e-04 pJ**, E_total = **0.9230 pJ** (0.04% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **1148** -> [mult.0.33.SVT20.syn.rpt:2434](../reports/SVT20/mult.0.33.SVT20.syn.rpt#L2434)
- Avg drive x**1.66**, D1 **69.3%**, D4+ **14.5%** of cells (29.4% of comb. area), largest **D12**
- Avg fan-in **2.62** (46.1% with 3+ inputs), FA/HA **28**, XOR/XNR **292**, complex AOI/OAI **332**, simple NAND/NOR **256**
- Recount drive strengths of the 1116 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.33.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.33.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 0.4125 ns (1.25x, 2424.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **819** -> [mult.0.4125.SVT20.syn_area.rpt:15](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.4125.SVT20.syn_area.rpt:17](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **133** -> [mult.0.4125.SVT20.syn_area.rpt:19](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **21.82** -> [mult.0.4125.SVT20.syn_area.rpt:23](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.4125.SVT20.syn_area.rpt:24](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L24)
- Total cell area = **365.58** -> [mult.0.4125.SVT20.syn_area.rpt:28](../reports/SVT20/mult.0.4125.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[13]** -> [mult.0.4125.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[26]** -> [mult.0.4125.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L17)
- Path cells = **13** (cell lines between [Point:26](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L26) and [data arrival:46](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L46), not counting the endpoint flop's D pin)
- Data arrival = **0.39 ns** -> [mult.0.4125.SVT20.syn_timing.rpt:46](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L46)
- Slack = **0.00 ns** -> [mult.0.4125.SVT20.syn_timing.rpt:58](../reports/SVT20/mult.0.4125.SVT20.syn_timing.rpt#L58)
- Path cells (function x drive), avg drive x1.0: `CKBx1 XNR2x1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 NR2x1 NR2x1 ND2x1 NR2x1 AOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.517 mW**, Int = **0.974 mW**, Leak = **533.531 nW** -> [mult.0.4125.SVT20.syn_power.rpt:41](../reports/SVT20/mult.0.4125.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.4125 = **0.6150 pJ**, E_leak = Leak/1e6 x 0.4125 = **2.201e-04 pJ**, E_total = **0.6153 pJ** (0.04% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **819** -> [mult.0.4125.SVT20.syn.rpt:1755](../reports/SVT20/mult.0.4125.SVT20.syn.rpt#L1755)
- Avg drive x**1.03**, D1 **97.7%**, D4+ **0.3%** of cells (0.4% of comb. area), largest **D4**
- Avg fan-in **2.68** (47.6% with 3+ inputs), FA/HA **117**, XOR/XNR **174**, complex AOI/OAI **200**, simple NAND/NOR **163**
- Recount drive strengths of the 787 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.4125.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.4125.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 0.495 ns (1.5x, 2020.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **770** -> [mult.0.495.SVT20.syn_area.rpt:15](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.495.SVT20.syn_area.rpt:17](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **117** -> [mult.0.495.SVT20.syn_area.rpt:19](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **18.87** -> [mult.0.495.SVT20.syn_area.rpt:23](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.495.SVT20.syn_area.rpt:24](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L24)
- Total cell area = **356.09** -> [mult.0.495.SVT20.syn_area.rpt:28](../reports/SVT20/mult.0.495.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[3]** -> [mult.0.495.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.495.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L17)
- Path cells = **21** (cell lines between [Point:26](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L26) and [data arrival:54](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L54), not counting the endpoint flop's D pin)
- Data arrival = **0.48 ns** -> [mult.0.495.SVT20.syn_timing.rpt:54](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L54)
- Slack = **0.00 ns** -> [mult.0.495.SVT20.syn_timing.rpt:66](../reports/SVT20/mult.0.495.SVT20.syn_timing.rpt#L66)
- Path cells (function x drive), avg drive x1.8: `BUFFx2 XNR2x1 ND2x1 INVx1 INVx1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 CKND2x1 OAI21x1 AOI21x1 OAI21x1 AOI21x2 OAI21x4 AOI21x4 OAI21x4 AOI21x4 OAI21x4 XNR2x1`

**syn_power.rpt**

- Switch = **0.412 mW**, Int = **0.803 mW**, Leak = **522.946 nW** -> [mult.0.495.SVT20.syn_power.rpt:41](../reports/SVT20/mult.0.495.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.495 = **0.6014 pJ**, E_leak = Leak/1e6 x 0.495 = **2.589e-04 pJ**, E_total = **0.6017 pJ** (0.04% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **770** -> [mult.0.495.SVT20.syn.rpt:1657](../reports/SVT20/mult.0.495.SVT20.syn.rpt#L1657)
- Avg drive x**1.02**, D1 **98.9%**, D4+ **0.7%** of cells (1.1% of comb. area), largest **D4**
- Avg fan-in **2.69** (47.3% with 3+ inputs), FA/HA **117**, XOR/XNR **174**, complex AOI/OAI **183**, simple NAND/NOR **147**
- Recount drive strengths of the 738 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.495.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.495.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 0.66 ns (2x, 1515.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **730** -> [mult.0.66.SVT20.syn_area.rpt:15](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.66.SVT20.syn_area.rpt:17](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **105** -> [mult.0.66.SVT20.syn_area.rpt:19](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **16.95** -> [mult.0.66.SVT20.syn_area.rpt:23](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.66.SVT20.syn_area.rpt:24](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L24)
- Total cell area = **348.16** -> [mult.0.66.SVT20.syn_area.rpt:28](../reports/SVT20/mult.0.66.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.0.66.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.66.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L17)
- Path cells = **29** (cell lines between [Point:26](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L26) and [data arrival:62](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L62), not counting the endpoint flop's D pin)
- Data arrival = **0.64 ns** -> [mult.0.66.SVT20.syn_timing.rpt:62](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L62)
- Slack = **0.00 ns** -> [mult.0.66.SVT20.syn_timing.rpt:74](../reports/SVT20/mult.0.66.SVT20.syn_timing.rpt#L74)
- Path cells (function x drive), avg drive x1.3: `XNR2x1 AN2x1 INVx1 OAI22x1 FA1x1 FA1x1 FA1x1 ND2x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x2 OAI21x4 AOI21x4 OAI21x1 AOI21x1 OAI21x1 AOI21x2 OAI21x2 AO21x1 FA1x1 FA1x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.294 mW**, Int = **0.597 mW**, Leak = **510.992 nW** -> [mult.0.66.SVT20.syn_power.rpt:41](../reports/SVT20/mult.0.66.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.66 = **0.5881 pJ**, E_leak = Leak/1e6 x 0.66 = **3.373e-04 pJ**, E_total = **0.5884 pJ** (0.06% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **730** -> [mult.0.66.SVT20.syn.rpt:1577](../reports/SVT20/mult.0.66.SVT20.syn.rpt#L1577)
- Avg drive x**1.02**, D1 **99.0%**, D4+ **0.3%** of cells (0.5% of comb. area), largest **D4**
- Avg fan-in **2.71** (48.1% with 3+ inputs), FA/HA **119**, XOR/XNR **173**, complex AOI/OAI **172**, simple NAND/NOR **129**
- Recount drive strengths of the 698 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.66.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.66.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 0.99 ns (3x, 1010.1 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **642** -> [mult.0.99.SVT20.syn_area.rpt:15](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.99.SVT20.syn_area.rpt:17](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **114** -> [mult.0.99.SVT20.syn_area.rpt:19](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **17.83** -> [mult.0.99.SVT20.syn_area.rpt:23](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.99.SVT20.syn_area.rpt:24](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L24)
- Total cell area = **327.42** -> [mult.0.99.SVT20.syn_area.rpt:28](../reports/SVT20/mult.0.99.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.0.99.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.99.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L26) and [data arrival:68](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.97 ns** -> [mult.0.99.SVT20.syn_timing.rpt:68](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L68)
- Slack = **0.00 ns** -> [mult.0.99.SVT20.syn_timing.rpt:80](../reports/SVT20/mult.0.99.SVT20.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x2.5: `NR2x1 AOI21x1 INVx1 NR2x1 INVx1 OAI32x1 OAI33x1 FA1x1 FA1x1 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x1 FA1x2 FA1x4 FA1x4 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x2 FA1x2 FA1x2 FA1x2 FA1x1 FA1x1 XNR4x1`

**syn_power.rpt**

- Switch = **0.196 mW**, Int = **0.379 mW**, Leak = **403.321 nW** -> [mult.0.99.SVT20.syn_power.rpt:41](../reports/SVT20/mult.0.99.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.99 = **0.5693 pJ**, E_leak = Leak/1e6 x 0.99 = **3.993e-04 pJ**, E_total = **0.5696 pJ** (0.07% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **642** -> [mult.0.99.SVT20.syn.rpt:1404](../reports/SVT20/mult.0.99.SVT20.syn.rpt#L1404)
- Avg drive x**1.09**, D1 **96.4%**, D4+ **2.5%** of cells (8.6% of comb. area), largest **D4**
- Avg fan-in **3.96** (83.9% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **273**, simple NAND/NOR **83**
- Recount drive strengths of the 610 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.99.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.0.99.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 1.65 ns (5x, 606.1 MHz) - first positive slack (Performance); netlist table row

**syn_area.rpt**

- Number of cells = **644** -> [mult.1.65.SVT20.syn_area.rpt:15](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.1.65.SVT20.syn_area.rpt:17](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **117** -> [mult.1.65.SVT20.syn_area.rpt:19](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **18.30** -> [mult.1.65.SVT20.syn_area.rpt:23](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.1.65.SVT20.syn_area.rpt:24](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L24)
- Total cell area = **317.99** -> [mult.1.65.SVT20.syn_area.rpt:28](../reports/SVT20/mult.1.65.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.1.65.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.1.65.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L17)
- Path cells = **36** (cell lines between [Point:26](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L26) and [data arrival:69](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L69), not counting the endpoint flop's D pin)
- Data arrival = **1.12 ns** -> [mult.1.65.SVT20.syn_timing.rpt:69](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L69)
- Slack = **0.51 ns** -> [mult.1.65.SVT20.syn_timing.rpt:81](../reports/SVT20/mult.1.65.SVT20.syn_timing.rpt#L81)
- Path cells (function x drive), avg drive x1.0: `NR2x1 AOI21x1 INVx1 NR2x1 INVx1 OAI32x1 OAI33x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR4x1`

**syn_power.rpt**

- Switch = **0.109 mW**, Int = **0.208 mW**, Leak = **367.875 nW** -> [mult.1.65.SVT20.syn_power.rpt:41](../reports/SVT20/mult.1.65.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 1.65 = **0.5231 pJ**, E_leak = Leak/1e6 x 1.65 = **6.070e-04 pJ**, E_total = **0.5237 pJ** (0.12% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **644** -> [mult.1.65.SVT20.syn.rpt:1408](../reports/SVT20/mult.1.65.SVT20.syn.rpt#L1408)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.97** (84.0% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **273**, simple NAND/NOR **82**
- Recount drive strengths of the 612 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.1.65.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.1.65.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 3.3 ns (10x, 303.0 MHz) - minimum E_total; netlist table row

**syn_area.rpt**

- Number of cells = **647** -> [mult.3.3.SVT20.syn_area.rpt:15](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.3.3.SVT20.syn_area.rpt:17](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **120** -> [mult.3.3.SVT20.syn_area.rpt:19](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **18.77** -> [mult.3.3.SVT20.syn_area.rpt:23](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.3.3.SVT20.syn_area.rpt:24](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L24)
- Total cell area = **318.19** -> [mult.3.3.SVT20.syn_area.rpt:28](../reports/SVT20/mult.3.3.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[3]** -> [mult.3.3.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.3.3.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L17)
- Path cells = **38** (cell lines between [Point:26](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L26) and [data arrival:71](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L71), not counting the endpoint flop's D pin)
- Data arrival = **1.12 ns** -> [mult.3.3.SVT20.syn_timing.rpt:71](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L71)
- Slack = **2.16 ns** -> [mult.3.3.SVT20.syn_timing.rpt:83](../reports/SVT20/mult.3.3.SVT20.syn_timing.rpt#L83)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 NR2x1 AOI21x1 ND2x1 INVx1 INVx1 OAI21x1 ND2x1 OAI21x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR4x1`

**syn_power.rpt**

- Switch = **0.055 mW**, Int = **0.103 mW**, Leak = **360.637 nW** -> [mult.3.3.SVT20.syn_power.rpt:41](../reports/SVT20/mult.3.3.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 3.3 = **0.5214 pJ**, E_leak = Leak/1e6 x 3.3 = **1.190e-03 pJ**, E_total = **0.5226 pJ** (0.23% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **647** -> [mult.3.3.SVT20.syn.rpt:1414](../reports/SVT20/mult.3.3.SVT20.syn.rpt#L1414)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.97** (84.0% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **273**, simple NAND/NOR **82**
- Recount drive strengths of the 615 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.3.3.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.3.3.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### SVT20 @ 330 ns (1000x, 3.0 MHz) - slowest clock ('relaxed' in the discussion); netlist table row

**syn_area.rpt**

- Number of cells = **647** -> [mult.330.SVT20.syn_area.rpt:15](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.330.SVT20.syn_area.rpt:17](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L17)
- Number of buf/inv = **120** -> [mult.330.SVT20.syn_area.rpt:19](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L19)
- Buf/Inv area = **18.77** -> [mult.330.SVT20.syn_area.rpt:23](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.330.SVT20.syn_area.rpt:24](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L24)
- Total cell area = **318.19** -> [mult.330.SVT20.syn_area.rpt:28](../reports/SVT20/mult.330.SVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[3]** -> [mult.330.SVT20.syn_timing.rpt:16](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.330.SVT20.syn_timing.rpt:17](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L17)
- Path cells = **37** (cell lines between [Point:26](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L26) and [data arrival:70](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L70), not counting the endpoint flop's D pin)
- Data arrival = **1.11 ns** -> [mult.330.SVT20.syn_timing.rpt:70](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L70)
- Slack = **328.87 ns** -> [mult.330.SVT20.syn_timing.rpt:82](../reports/SVT20/mult.330.SVT20.syn_timing.rpt#L82)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 NR2x1 AOI21x1 ND2x1 INVx1 INVx1 OAI32x1 OAI33x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR4x1`

**syn_power.rpt**

- Switch = **0.00055 mW**, Int = **0.00103 mW**, Leak = **360.637 nW** -> [mult.330.SVT20.syn_power.rpt:41](../reports/SVT20/mult.330.SVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 330 = **0.5214 pJ**, E_leak = Leak/1e6 x 330 = **1.190e-01 pJ**, E_total = **0.6404 pJ** (18.58% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **647** -> [mult.330.SVT20.syn.rpt:1414](../reports/SVT20/mult.330.SVT20.syn.rpt#L1414)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.97** (84.0% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **273**, simple NAND/NOR **82**
- Recount drive strengths of the 615 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.330.SVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/SVT20/mult.330.SVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

## LVT20

- F_max point: 0.244 ns; slowest point: 244 ns
- First positive slack: 1.22 ns
- Minimum E_total: 0.5699 pJ at 2.44 ns (check against `reports/LVT20/energy.csv`)

### LVT20 @ 0.244 ns (1x, 4098.4 MHz) - F_max (Performance / Drive strength / critical-path list); netlist table row

**syn_area.rpt**

- Number of cells = **1254** -> [mult.0.244.LVT20.syn_area.rpt:15](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.244.LVT20.syn_area.rpt:17](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **213** -> [mult.0.244.LVT20.syn_area.rpt:19](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **43.70** -> [mult.0.244.LVT20.syn_area.rpt:23](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.244.LVT20.syn_area.rpt:24](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L24)
- Total cell area = **525.24** -> [mult.0.244.LVT20.syn_area.rpt:28](../reports/LVT20/mult.0.244.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.0.244.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[26]** -> [mult.0.244.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L17)
- Path cells = **17** (cell lines between [Point:26](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L26) and [data arrival:50](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L50), not counting the endpoint flop's D pin)
- Data arrival = **0.23 ns** -> [mult.0.244.LVT20.syn_timing.rpt:50](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L50)
- Slack = **0.00 ns** -> [mult.0.244.LVT20.syn_timing.rpt:62](../reports/LVT20/mult.0.244.LVT20.syn_timing.rpt#L62)
- Path cells (function x drive), avg drive x2.3: `CKBx1 XNR2x1 OAI22x1 XOR2x1 XOR2x2 XNR2x2 XNR2x4 ND2x1 INVx1 AOI21x1 ND2x2 AOI21x4 OAI21x8 AOI21x4 OAI21x4 AOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **1.349 mW**, Int = **2.706 mW**, Leak = **13400 nW** -> [mult.0.244.LVT20.syn_power.rpt:41](../reports/LVT20/mult.0.244.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.244 = **0.9894 pJ**, E_leak = Leak/1e6 x 0.244 = **3.270e-03 pJ**, E_total = **0.9927 pJ** (0.33% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **1254** -> [mult.0.244.LVT20.syn.rpt:3879](../reports/LVT20/mult.0.244.LVT20.syn.rpt#L3879)
- Avg drive x**1.56**, D1 **73.1%**, D4+ **10.4%** of cells (20.4% of comb. area), largest **D12**
- Avg fan-in **2.51** (37.4% with 3+ inputs), FA/HA **17**, XOR/XNR **372**, complex AOI/OAI **353**, simple NAND/NOR **267**
- Recount drive strengths of the 1222 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.244.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.244.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 0.305 ns (1.25x, 3278.7 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **820** -> [mult.0.305.LVT20.syn_area.rpt:15](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.305.LVT20.syn_area.rpt:17](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **127** -> [mult.0.305.LVT20.syn_area.rpt:19](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **21.77** -> [mult.0.305.LVT20.syn_area.rpt:23](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.305.LVT20.syn_area.rpt:24](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L24)
- Total cell area = **367.70** -> [mult.0.305.LVT20.syn_area.rpt:28](../reports/LVT20/mult.0.305.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[7]** -> [mult.0.305.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[21]** -> [mult.0.305.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L17)
- Path cells = **14** (cell lines between [Point:26](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L26) and [data arrival:47](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L47), not counting the endpoint flop's D pin)
- Data arrival = **0.29 ns** -> [mult.0.305.LVT20.syn_timing.rpt:47](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L47)
- Slack = **0.00 ns** -> [mult.0.305.LVT20.syn_timing.rpt:59](../reports/LVT20/mult.0.305.LVT20.syn_timing.rpt#L59)
- Path cells (function x drive), avg drive x1.3: `CKBx1 XOR2x1 INVx1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 NR2x1 NR2x1 ND2x2 OAI21x4 AOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.736 mW**, Int = **1.484 mW**, Leak = **6750 nW** -> [mult.0.305.LVT20.syn_power.rpt:41](../reports/LVT20/mult.0.305.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.305 = **0.6771 pJ**, E_leak = Leak/1e6 x 0.305 = **2.059e-03 pJ**, E_total = **0.6792 pJ** (0.30% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **820** -> [mult.0.305.LVT20.syn.rpt:2577](../reports/LVT20/mult.0.305.LVT20.syn.rpt#L2577)
- Avg drive x**1.05**, D1 **97.0%**, D4+ **0.6%** of cells (0.9% of comb. area), largest **D8**
- Avg fan-in **2.67** (47.0% with 3+ inputs), FA/HA **116**, XOR/XNR **176**, complex AOI/OAI **201**, simple NAND/NOR **168**
- Recount drive strengths of the 788 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.305.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.305.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 0.366 ns (1.5x, 2732.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **776** -> [mult.0.366.LVT20.syn_area.rpt:15](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.366.LVT20.syn_area.rpt:17](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **116** -> [mult.0.366.LVT20.syn_area.rpt:19](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **18.71** -> [mult.0.366.LVT20.syn_area.rpt:23](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.366.LVT20.syn_area.rpt:24](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L24)
- Total cell area = **355.52** -> [mult.0.366.LVT20.syn_area.rpt:28](../reports/LVT20/mult.0.366.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[7]** -> [mult.0.366.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.366.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L17)
- Path cells = **18** (cell lines between [Point:26](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L26) and [data arrival:51](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L51), not counting the endpoint flop's D pin)
- Data arrival = **0.35 ns** -> [mult.0.366.LVT20.syn_timing.rpt:51](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L51)
- Slack = **0.00 ns** -> [mult.0.366.LVT20.syn_timing.rpt:63](../reports/LVT20/mult.0.366.LVT20.syn_timing.rpt#L63)
- Path cells (function x drive), avg drive x1.2: `XNR2x1 CKND2x1 CKBx1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 ND2x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x4 AOI21x1 OAI21x2 AOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.57 mW**, Int = **1.215 mW**, Leak = **6490 nW** -> [mult.0.366.LVT20.syn_power.rpt:41](../reports/LVT20/mult.0.366.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.366 = **0.6533 pJ**, E_leak = Leak/1e6 x 0.366 = **2.375e-03 pJ**, E_total = **0.6557 pJ** (0.36% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **776** -> [mult.0.366.LVT20.syn.rpt:2445](../reports/LVT20/mult.0.366.LVT20.syn.rpt#L2445)
- Avg drive x**1.01**, D1 **99.6%**, D4+ **0.1%** of cells (0.2% of comb. area), largest **D4**
- Avg fan-in **2.69** (47.5% with 3+ inputs), FA/HA **115**, XOR/XNR **178**, complex AOI/OAI **189**, simple NAND/NOR **146**
- Recount drive strengths of the 744 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.366.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.366.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 0.488 ns (2x, 2049.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **732** -> [mult.0.488.LVT20.syn_area.rpt:15](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.488.LVT20.syn_area.rpt:17](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **105** -> [mult.0.488.LVT20.syn_area.rpt:19](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **17.11** -> [mult.0.488.LVT20.syn_area.rpt:23](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.488.LVT20.syn_area.rpt:24](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L24)
- Total cell area = **346.91** -> [mult.0.488.LVT20.syn_area.rpt:28](../reports/LVT20/mult.0.488.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[15]** -> [mult.0.488.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.488.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L17)
- Path cells = **27** (cell lines between [Point:26](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L26) and [data arrival:60](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L60), not counting the endpoint flop's D pin)
- Data arrival = **0.47 ns** -> [mult.0.488.LVT20.syn_timing.rpt:60](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L60)
- Slack = **0.00 ns** -> [mult.0.488.LVT20.syn_timing.rpt:72](../reports/LVT20/mult.0.488.LVT20.syn_timing.rpt#L72)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 XOR2x1 AN2x1 INVx1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 OR2x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 MAOI222x1 XNR2x1`

**syn_power.rpt**

- Switch = **0.407 mW**, Int = **0.896 mW**, Leak = **6300 nW** -> [mult.0.488.LVT20.syn_power.rpt:41](../reports/LVT20/mult.0.488.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.488 = **0.6359 pJ**, E_leak = Leak/1e6 x 0.488 = **3.074e-03 pJ**, E_total = **0.6389 pJ** (0.48% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **732** -> [mult.0.488.LVT20.syn.rpt:2313](../reports/LVT20/mult.0.488.LVT20.syn.rpt#L2313)
- Avg drive x**1.01**, D1 **99.4%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D2**
- Avg fan-in **2.71** (47.9% with 3+ inputs), FA/HA **118**, XOR/XNR **174**, complex AOI/OAI **173**, simple NAND/NOR **130**
- Recount drive strengths of the 700 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.488.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.488.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 0.732 ns (3x, 1366.1 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.0.732.LVT20.syn_area.rpt:15](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.732.LVT20.syn_area.rpt:17](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **107** -> [mult.0.732.LVT20.syn_area.rpt:19](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **16.74** -> [mult.0.732.LVT20.syn_area.rpt:23](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.732.LVT20.syn_area.rpt:24](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L24)
- Total cell area = **320.11** -> [mult.0.732.LVT20.syn_area.rpt:28](../reports/LVT20/mult.0.732.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.0.732.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.732.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L26) and [data arrival:68](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.71 ns** -> [mult.0.732.LVT20.syn_timing.rpt:68](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L68)
- Slack = **0.00 ns** -> [mult.0.732.LVT20.syn_timing.rpt:80](../reports/LVT20/mult.0.732.LVT20.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x2.4: `INVx1 INVx1 AOI22x1 AOI33x1 ND2x1 OAI21x1 FA1x2 FA1x2 FA1x2 FA1x2 FA1x1 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x1 FA1x4 FA1x4 FA1x4 FA1x4 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x2 FA1x1 FA1x1 FA1x1 FA1x1 FA1x2 XNR3x1`

**syn_power.rpt**

- Switch = **0.27 mW**, Int = **0.587 mW**, Leak = **5260 nW** -> [mult.0.732.LVT20.syn_power.rpt:41](../reports/LVT20/mult.0.732.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.732 = **0.6273 pJ**, E_leak = Leak/1e6 x 0.732 = **3.850e-03 pJ**, E_total = **0.6312 pJ** (0.61% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.0.732.LVT20.syn.rpt:2002](../reports/LVT20/mult.0.732.LVT20.syn.rpt#L2002)
- Avg drive x**1.08**, D1 **96.3%**, D4+ **2.3%** of cells (8.2% of comb. area), largest **D4**
- Avg fan-in **3.83** (88.5% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **280**, simple NAND/NOR **69**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.732.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.0.732.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 1.22 ns (5x, 819.7 MHz) - first positive slack (Performance); netlist table row

**syn_area.rpt**

- Number of cells = **626** -> [mult.1.22.LVT20.syn_area.rpt:15](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.1.22.LVT20.syn_area.rpt:17](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **108** -> [mult.1.22.LVT20.syn_area.rpt:19](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **16.90** -> [mult.1.22.LVT20.syn_area.rpt:23](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.1.22.LVT20.syn_area.rpt:24](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L24)
- Total cell area = **310.47** -> [mult.1.22.LVT20.syn_area.rpt:28](../reports/LVT20/mult.1.22.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.1.22.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.1.22.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L17)
- Path cells = **33** (cell lines between [Point:26](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L26) and [data arrival:66](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L66), not counting the endpoint flop's D pin)
- Data arrival = **0.82 ns** -> [mult.1.22.LVT20.syn_timing.rpt:66](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L66)
- Slack = **0.38 ns** -> [mult.1.22.LVT20.syn_timing.rpt:78](../reports/LVT20/mult.1.22.LVT20.syn_timing.rpt#L78)
- Path cells (function x drive), avg drive x1.0: `MAOI22x1 ND2x1 AOI22x1 OAI33x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x2`

**syn_power.rpt**

- Switch = **0.151 mW**, Int = **0.312 mW**, Leak = **4740 nW** -> [mult.1.22.LVT20.syn_power.rpt:41](../reports/LVT20/mult.1.22.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 1.22 = **0.5649 pJ**, E_leak = Leak/1e6 x 1.22 = **5.783e-03 pJ**, E_total = **0.5706 pJ** (1.01% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **626** -> [mult.1.22.LVT20.syn.rpt:1996](../reports/LVT20/mult.1.22.LVT20.syn.rpt#L1996)
- Avg drive x**1.00**, D1 **99.8%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D2**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 594 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.1.22.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.1.22.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 2.44 ns (10x, 409.8 MHz) - minimum E_total; netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.2.44.LVT20.syn_area.rpt:15](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.2.44.LVT20.syn_area.rpt:17](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **110** -> [mult.2.44.LVT20.syn_area.rpt:19](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **17.21** -> [mult.2.44.LVT20.syn_area.rpt:23](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.2.44.LVT20.syn_area.rpt:24](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L24)
- Total cell area = **310.73** -> [mult.2.44.LVT20.syn_area.rpt:28](../reports/LVT20/mult.2.44.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.2.44.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.2.44.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L26) and [data arrival:68](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.82 ns** -> [mult.2.44.LVT20.syn_timing.rpt:68](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L68)
- Slack = **1.61 ns** -> [mult.2.44.LVT20.syn_timing.rpt:80](../reports/LVT20/mult.2.44.LVT20.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 AOI22x1 AOI33x1 ND2x1 OAI21x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x1`

**syn_power.rpt**

- Switch = **0.0749 mW**, Int = **0.154 mW**, Leak = **4660 nW** -> [mult.2.44.LVT20.syn_power.rpt:41](../reports/LVT20/mult.2.44.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 2.44 = **0.5585 pJ**, E_leak = Leak/1e6 x 2.44 = **1.137e-02 pJ**, E_total = **0.5699 pJ** (2.00% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.2.44.LVT20.syn.rpt:2002](../reports/LVT20/mult.2.44.LVT20.syn.rpt#L2002)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.2.44.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.2.44.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT20 @ 244 ns (1000x, 4.1 MHz) - slowest clock ('relaxed' in the discussion); netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.244.LVT20.syn_area.rpt:15](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.244.LVT20.syn_area.rpt:17](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L17)
- Number of buf/inv = **110** -> [mult.244.LVT20.syn_area.rpt:19](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L19)
- Buf/Inv area = **17.21** -> [mult.244.LVT20.syn_area.rpt:23](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.244.LVT20.syn_area.rpt:24](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L24)
- Total cell area = **310.73** -> [mult.244.LVT20.syn_area.rpt:28](../reports/LVT20/mult.244.LVT20.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.244.LVT20.syn_timing.rpt:16](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.244.LVT20.syn_timing.rpt:17](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L17)
- Path cells = **33** (cell lines between [Point:26](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L26) and [data arrival:66](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L66), not counting the endpoint flop's D pin)
- Data arrival = **0.82 ns** -> [mult.244.LVT20.syn_timing.rpt:66](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L66)
- Slack = **243.17 ns** -> [mult.244.LVT20.syn_timing.rpt:78](../reports/LVT20/mult.244.LVT20.syn_timing.rpt#L78)
- Path cells (function x drive), avg drive x1.0: `MAOI22x1 ND2x1 AOI22x1 OAI33x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x1`

**syn_power.rpt**

- Switch = **0.000748 mW**, Int = **0.00154 mW**, Leak = **4660 nW** -> [mult.244.LVT20.syn_power.rpt:41](../reports/LVT20/mult.244.LVT20.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 244 = **0.5583 pJ**, E_leak = Leak/1e6 x 244 = **1.137e+00 pJ**, E_total = **1.6953 pJ** (67.07% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.244.LVT20.syn.rpt:2002](../reports/LVT20/mult.244.LVT20.syn.rpt#L2002)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.244.LVT20.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT20/mult.244.LVT20.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

## LVT16

- F_max point: 0.22 ns; slowest point: 220 ns
- First positive slack: 1.1 ns
- Minimum E_total: 0.5662 pJ at 1.1 ns (check against `reports/LVT16/energy.csv`)

### LVT16 @ 0.22 ns (1x, 4545.5 MHz) - F_max (Performance / Drive strength / critical-path list); netlist table row

**syn_area.rpt**

- Number of cells = **1359** -> [mult.0.22.LVT16.syn_area.rpt:15](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.22.LVT16.syn_area.rpt:17](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **336** -> [mult.0.22.LVT16.syn_area.rpt:19](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **67.03** -> [mult.0.22.LVT16.syn_area.rpt:23](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.22.LVT16.syn_area.rpt:24](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L24)
- Total cell area = **629.75** -> [mult.0.22.LVT16.syn_area.rpt:28](../reports/LVT16/mult.0.22.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[13]** -> [mult.0.22.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[27]** -> [mult.0.22.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L17)
- Path cells = **19** (cell lines between [Point:26](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L26) and [data arrival:52](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L52), not counting the endpoint flop's D pin)
- Data arrival = **0.20 ns** -> [mult.0.22.LVT16.syn_timing.rpt:52](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L52)
- Slack = **0.00 ns** -> [mult.0.22.LVT16.syn_timing.rpt:64](../reports/LVT16/mult.0.22.LVT16.syn_timing.rpt#L64)
- Path cells (function x drive), avg drive x3.7: `CKNx2 INVx4 BUFFx4 XNR2x1 NR2x2 NR2x4 XNR2x4 XNR2x8 XOR2x8 XOR2x4 XNR2x4 ND2x2 INVx1 AOI21x4 OAI21x4 AOI21x8 OAI21x4 AOI21x1 XNR2x1`

**syn_power.rpt**

- Switch = **1.696 mW**, Int = **3.802 mW**, Leak = **43200 nW** -> [mult.0.22.LVT16.syn_power.rpt:41](../reports/LVT16/mult.0.22.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.22 = **1.2096 pJ**, E_leak = Leak/1e6 x 0.22 = **9.504e-03 pJ**, E_total = **1.2191 pJ** (0.78% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **1359** -> [mult.0.22.LVT16.syn.rpt:4194](../reports/LVT16/mult.0.22.LVT16.syn.rpt#L4194)
- Avg drive x**1.94**, D1 **60.2%**, D4+ **22.2%** of cells (44.9% of comb. area), largest **D16**
- Avg fan-in **2.56** (38.3% with 3+ inputs), FA/HA **18**, XOR/XNR **302**, complex AOI/OAI **289**, simple NAND/NOR **382**
- Recount drive strengths of the 1327 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.22.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.22.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 0.275 ns (1.25x, 3636.4 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **839** -> [mult.0.275.LVT16.syn_area.rpt:15](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.275.LVT16.syn_area.rpt:17](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **136** -> [mult.0.275.LVT16.syn_area.rpt:19](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **22.65** -> [mult.0.275.LVT16.syn_area.rpt:23](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.275.LVT16.syn_area.rpt:24](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L24)
- Total cell area = **369.98** -> [mult.0.275.LVT16.syn_area.rpt:28](../reports/LVT16/mult.0.275.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[5]** -> [mult.0.275.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[22]** -> [mult.0.275.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L17)
- Path cells = **14** (cell lines between [Point:26](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L26) and [data arrival:47](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L47), not counting the endpoint flop's D pin)
- Data arrival = **0.26 ns** -> [mult.0.275.LVT16.syn_timing.rpt:47](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L47)
- Slack = **0.00 ns** -> [mult.0.275.LVT16.syn_timing.rpt:59](../reports/LVT16/mult.0.275.LVT16.syn_timing.rpt#L59)
- Path cells (function x drive), avg drive x1.2: `CKBx1 XNR2x1 ND2x1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 CKNR2x1 OAI21x1 AOI21x1 OAI21x4 AOI21x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.764 mW**, Int = **1.65 mW**, Leak = **15700 nW** -> [mult.0.275.LVT16.syn_power.rpt:41](../reports/LVT16/mult.0.275.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.275 = **0.6639 pJ**, E_leak = Leak/1e6 x 0.275 = **4.318e-03 pJ**, E_total = **0.6682 pJ** (0.65% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **839** -> [mult.0.275.LVT16.syn.rpt:2634](../reports/LVT16/mult.0.275.LVT16.syn.rpt#L2634)
- Avg drive x**1.03**, D1 **97.1%**, D4+ **0.2%** of cells (0.4% of comb. area), largest **D4**
- Avg fan-in **2.66** (46.3% with 3+ inputs), FA/HA **113**, XOR/XNR **180**, complex AOI/OAI **202**, simple NAND/NOR **176**
- Recount drive strengths of the 807 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.275.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.275.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 0.33 ns (1.5x, 3030.3 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **770** -> [mult.0.33.LVT16.syn_area.rpt:15](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.33.LVT16.syn_area.rpt:17](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **121** -> [mult.0.33.LVT16.syn_area.rpt:19](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **19.70** -> [mult.0.33.LVT16.syn_area.rpt:23](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.33.LVT16.syn_area.rpt:24](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L24)
- Total cell area = **359.61** -> [mult.0.33.LVT16.syn_area.rpt:28](../reports/LVT16/mult.0.33.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[11]** -> [mult.0.33.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.33.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L17)
- Path cells = **23** (cell lines between [Point:26](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L26) and [data arrival:56](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L56), not counting the endpoint flop's D pin)
- Data arrival = **0.31 ns** -> [mult.0.33.LVT16.syn_timing.rpt:56](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L56)
- Slack = **0.00 ns** -> [mult.0.33.LVT16.syn_timing.rpt:68](../reports/LVT16/mult.0.33.LVT16.syn_timing.rpt#L68)
- Path cells (function x drive), avg drive x2.2: `INVx1 CKNx2 XNR2x4 AN2x1 INVx1 OAI22x1 FA1x1 FA1x1 FA1x1 FA1x1 CKND2x1 OAI21x1 AOI21x1 OAI21x2 AOI21x4 OAI21x4 AOI21x4 OAI21x4 AOI21x4 OAI21x4 AOI21x4 OAI21x2 XNR2x1`

**syn_power.rpt**

- Switch = **0.607 mW**, Int = **1.36 mW**, Leak = **15600 nW** -> [mult.0.33.LVT16.syn_power.rpt:41](../reports/LVT16/mult.0.33.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.33 = **0.6491 pJ**, E_leak = Leak/1e6 x 0.33 = **5.148e-03 pJ**, E_total = **0.6543 pJ** (0.79% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **770** -> [mult.0.33.LVT16.syn.rpt:2427](../reports/LVT16/mult.0.33.LVT16.syn.rpt#L2427)
- Avg drive x**1.07**, D1 **96.5%**, D4+ **1.9%** of cells (3.5% of comb. area), largest **D4**
- Avg fan-in **2.69** (47.3% with 3+ inputs), FA/HA **117**, XOR/XNR **174**, complex AOI/OAI **181**, simple NAND/NOR **145**
- Recount drive strengths of the 738 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.33.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.33.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 0.44 ns (2x, 2272.7 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **717** -> [mult.0.44.LVT16.syn_area.rpt:15](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.44.LVT16.syn_area.rpt:17](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **103** -> [mult.0.44.LVT16.syn_area.rpt:19](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **16.64** -> [mult.0.44.LVT16.syn_area.rpt:23](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.44.LVT16.syn_area.rpt:24](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L24)
- Total cell area = **350.28** -> [mult.0.44.LVT16.syn_area.rpt:28](../reports/LVT16/mult.0.44.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[3]** -> [mult.0.44.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.44.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L17)
- Path cells = **36** (cell lines between [Point:26](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L26) and [data arrival:69](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L69), not counting the endpoint flop's D pin)
- Data arrival = **0.42 ns** -> [mult.0.44.LVT16.syn_timing.rpt:69](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L69)
- Slack = **0.00 ns** -> [mult.0.44.LVT16.syn_timing.rpt:81](../reports/LVT16/mult.0.44.LVT16.syn_timing.rpt#L81)
- Path cells (function x drive), avg drive x1.9: `BUFFx2 XNR2x1 INVx1 INVx1 OAI22x1 HA1x1 FA1x1 ND2x1 OA21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x1 AOI21x1 OAI21x2 AOI21x1 OAI21x1 AOI21x1 OAI21x2 AOI21x2 OAI21x4 AOI21x4 OAI21x4 AOI21x4 OAI21x4 AOI21x4 OAI21x2 ND2x2 IND2x2 FA1x4 FA1x4 FA1x1 XOR2x1`

**syn_power.rpt**

- Switch = **0.444 mW**, Int = **1.033 mW**, Leak = **15000 nW** -> [mult.0.44.LVT16.syn_power.rpt:41](../reports/LVT16/mult.0.44.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.44 = **0.6499 pJ**, E_leak = Leak/1e6 x 0.44 = **6.600e-03 pJ**, E_total = **0.6565 pJ** (1.01% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **717** -> [mult.0.44.LVT16.syn.rpt:2268](../reports/LVT16/mult.0.44.LVT16.syn.rpt#L2268)
- Avg drive x**1.06**, D1 **96.9%**, D4+ **1.5%** of cells (3.0% of comb. area), largest **D4**
- Avg fan-in **2.72** (48.5% with 3+ inputs), FA/HA **121**, XOR/XNR **170**, complex AOI/OAI **167**, simple NAND/NOR **124**
- Recount drive strengths of the 685 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.44.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.44.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 0.66 ns (3x, 1515.2 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **625** -> [mult.0.66.LVT16.syn_area.rpt:15](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.0.66.LVT16.syn_area.rpt:17](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **107** -> [mult.0.66.LVT16.syn_area.rpt:19](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **16.74** -> [mult.0.66.LVT16.syn_area.rpt:23](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.0.66.LVT16.syn_area.rpt:24](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L24)
- Total cell area = **318.97** -> [mult.0.66.LVT16.syn_area.rpt:28](../reports/LVT16/mult.0.66.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.0.66.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.0.66.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L26) and [data arrival:68](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.64 ns** -> [mult.0.66.LVT16.syn_timing.rpt:68](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L68)
- Slack = **0.00 ns** -> [mult.0.66.LVT16.syn_timing.rpt:80](../reports/LVT16/mult.0.66.LVT16.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x2.3: `INVx1 INVx1 AOI22x1 AOI33x1 ND2x1 OAI21x1 FA1x1 FA1x1 FA1x1 FA1x2 FA1x2 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x1 FA1x2 FA1x4 FA1x4 FA1x4 FA1x2 FA1x4 FA1x4 FA1x4 FA1x4 FA1x4 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x2 XNR3x1`

**syn_power.rpt**

- Switch = **0.281 mW**, Int = **0.655 mW**, Leak = **11900 nW** -> [mult.0.66.LVT16.syn_power.rpt:41](../reports/LVT16/mult.0.66.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 0.66 = **0.6178 pJ**, E_leak = Leak/1e6 x 0.66 = **7.854e-03 pJ**, E_total = **0.6256 pJ** (1.26% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **625** -> [mult.0.66.LVT16.syn.rpt:1993](../reports/LVT16/mult.0.66.LVT16.syn.rpt#L1993)
- Avg drive x**1.08**, D1 **96.8%**, D4+ **2.2%** of cells (7.6% of comb. area), largest **D4**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 593 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.66.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.0.66.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 1.1 ns (5x, 909.1 MHz) - first positive slack (Performance); minimum E_total; netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.1.1.LVT16.syn_area.rpt:15](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.1.1.LVT16.syn_area.rpt:17](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **110** -> [mult.1.1.LVT16.syn_area.rpt:19](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **17.21** -> [mult.1.1.LVT16.syn_area.rpt:23](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.1.1.LVT16.syn_area.rpt:24](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L24)
- Total cell area = **310.73** -> [mult.1.1.LVT16.syn_area.rpt:28](../reports/LVT16/mult.1.1.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.1.1.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.1.1.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L26) and [data arrival:68](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.73 ns** -> [mult.1.1.LVT16.syn_timing.rpt:68](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L68)
- Slack = **0.36 ns** -> [mult.1.1.LVT16.syn_timing.rpt:80](../reports/LVT16/mult.1.1.LVT16.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 AOI22x1 AOI33x1 ND2x1 OAI21x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x1`

**syn_power.rpt**

- Switch = **0.158 mW**, Int = **0.346 mW**, Leak = **10700 nW** -> [mult.1.1.LVT16.syn_power.rpt:41](../reports/LVT16/mult.1.1.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 1.1 = **0.5544 pJ**, E_leak = Leak/1e6 x 1.1 = **1.177e-02 pJ**, E_total = **0.5662 pJ** (2.08% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.1.1.LVT16.syn.rpt:2002](../reports/LVT16/mult.1.1.LVT16.syn.rpt#L2002)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.1.1.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.1.1.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 2.2 ns (10x, 454.5 MHz) - netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.2.2.LVT16.syn_area.rpt:15](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.2.2.LVT16.syn_area.rpt:17](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **110** -> [mult.2.2.LVT16.syn_area.rpt:19](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **17.21** -> [mult.2.2.LVT16.syn_area.rpt:23](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.2.2.LVT16.syn_area.rpt:24](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L24)
- Total cell area = **310.73** -> [mult.2.2.LVT16.syn_area.rpt:28](../reports/LVT16/mult.2.2.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_b[0]** -> [mult.2.2.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.2.2.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L17)
- Path cells = **35** (cell lines between [Point:26](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L26) and [data arrival:68](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L68), not counting the endpoint flop's D pin)
- Data arrival = **0.73 ns** -> [mult.2.2.LVT16.syn_timing.rpt:68](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L68)
- Slack = **1.46 ns** -> [mult.2.2.LVT16.syn_timing.rpt:80](../reports/LVT16/mult.2.2.LVT16.syn_timing.rpt#L80)
- Path cells (function x drive), avg drive x1.0: `INVx1 INVx1 AOI22x1 AOI33x1 ND2x1 OAI21x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x1`

**syn_power.rpt**

- Switch = **0.079 mW**, Int = **0.173 mW**, Leak = **10700 nW** -> [mult.2.2.LVT16.syn_power.rpt:41](../reports/LVT16/mult.2.2.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 2.2 = **0.5544 pJ**, E_leak = Leak/1e6 x 2.2 = **2.354e-02 pJ**, E_total = **0.5779 pJ** (4.07% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.2.2.LVT16.syn.rpt:2002](../reports/LVT16/mult.2.2.LVT16.syn.rpt#L2002)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.2.2.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.2.2.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

### LVT16 @ 220 ns (1000x, 4.5 MHz) - slowest clock ('relaxed' in the discussion); netlist table row

**syn_area.rpt**

- Number of cells = **628** -> [mult.220.LVT16.syn_area.rpt:15](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L15)
- Number of sequential cells = **32** -> [mult.220.LVT16.syn_area.rpt:17](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L17)
- Number of buf/inv = **110** -> [mult.220.LVT16.syn_area.rpt:19](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L19)
- Buf/Inv area = **17.21** -> [mult.220.LVT16.syn_area.rpt:23](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L23)
- Noncombinational area = **36.50** -> [mult.220.LVT16.syn_area.rpt:24](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L24)
- Total cell area = **310.73** -> [mult.220.LVT16.syn_area.rpt:28](../reports/LVT16/mult.220.LVT16.syn_area.rpt#L28)

**syn_timing.rpt** (first path = worst path)

- Startpoint = **inp_a[1]** -> [mult.220.LVT16.syn_timing.rpt:16](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L16)
- Endpoint = **prod_reg[31]** -> [mult.220.LVT16.syn_timing.rpt:17](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L17)
- Path cells = **33** (cell lines between [Point:26](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L26) and [data arrival:66](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L66), not counting the endpoint flop's D pin)
- Data arrival = **0.73 ns** -> [mult.220.LVT16.syn_timing.rpt:66](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L66)
- Slack = **219.26 ns** -> [mult.220.LVT16.syn_timing.rpt:78](../reports/LVT16/mult.220.LVT16.syn_timing.rpt#L78)
- Path cells (function x drive), avg drive x1.0: `MAOI22x1 ND2x1 AOI22x1 OAI33x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 FA1x1 XNR3x1`

**syn_power.rpt**

- Switch = **0.000785 mW**, Int = **0.0017 mW**, Leak = **10400 nW** -> [mult.220.LVT16.syn_power.rpt:41](../reports/LVT16/mult.220.LVT16.syn_power.rpt#L41)
- E_dyn = (Switch + Int) x 220 = **0.5467 pJ**, E_leak = Leak/1e6 x 220 = **2.288e+00 pJ**, E_total = **2.8347 pJ** (80.71% leakage)

**syn.rpt** (counted from the cell list; no single line)

- Total cells = **628** -> [mult.220.LVT16.syn.rpt:2002](../reports/LVT16/mult.220.LVT16.syn.rpt#L2002)
- Avg drive x**1.00**, D1 **100.0%**, D4+ **0.0%** of cells (0.0% of comb. area), largest **D1**
- Avg fan-in **3.85** (89.3% with 3+ inputs), FA/HA **139**, XOR/XNR **1**, complex AOI/OAI **281**, simple NAND/NOR **65**
- Recount drive strengths of the 596 combinational cells (run in `synthesis/lab2/`):
  `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.220.LVT16.syn.rpt | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\1/' | sort | uniq -c`
- Recount adders: `sed -n '/^Report : cell/,/^Total .* cells/p' reports/LVT16/mult.220.LVT16.syn.rpt | grep -cE '\b(FA1|HA1)D[0-9]+BWP'`

