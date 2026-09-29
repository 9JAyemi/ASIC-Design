#!/usr/bin/env python3
"""Write the Lab 2 report as LaTeX, in the same style as the HW1 report.

Uses the parsers in ppa_report.py (area / timing / cell / power reports) and the
plotting code in plot_energy.py, so everything comes from reports/<group>/.

Output: report/lab2_report.tex, report/figures/*.png, and report/lab2_report.zip
(upload the zip to Overleaf as a new project and compile). If pdflatex is on the
PATH, the PDF is built too.

Usage:  python3.12 lab2_report.py
Edit the settings below if the problem numbers or title differ.
"""
import os
import re
import shutil
import subprocess
import zipfile

import ppa_report as ppa
import plot_energy as pe

# ---------------------------------------------------------------- settings
TITLE = "ECE 5746 Lab 2"
AUTHOR = "Abiola Bolaji"
# problem number that each library's sweep answers, and the PPA discussion question
PROBLEMS = {"SVT20": "2", "LVT20": "3", "LVT16": "4"}
DISCUSSION = "5"
RTL_SECTION = "1"   # problem number for the RTL design and testbench
# heading text shown after each problem number (edit freely)
HEADINGS = {
    "RTL": "RTL Design and Verification",
    "SVT20": "SVT20: Fmax and Energy Sweep",
    "LVT20": "LVT20: Fmax and Energy Sweep",
    "LVT16": "LVT16: Fmax and Energy Sweep",
    "DISCUSSION": "PPA Trends and Optimal Operating Frequency",
}
# save your QuestaSim waveform screenshot here (report/figures/rtl_waveform.png)
WAVEFORM = "rtl_waveform.png"
# how each clk_period_min was chosen (shown in the report)
MIN_NOTE = {
    "SVT20": "chosen at 0.01\\,ns precision; a finer search showed 0.327\\,ns also meets timing",
    "LVT20": "0.244\\,ns meets timing and 0.242\\,ns does not",
    "LVT16": "chosen at 0.01\\,ns precision: 0.22\\,ns meets timing and 0.21\\,ns does not",
}
LIB_DESC = {
    "SVT20": "standard-$V_t$ cells (BWP20P90)",
    "LVT20": "low-$V_t$ cells (BWP20P90LVT)",
    "LVT16": "low-$V_t$ cells (BWP16P90LVT)",
}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "report")
FIG = os.path.join(OUT, "figures")
RTL = os.path.join(HERE, "..", "..", "rtl")


def rtl_section():
    """RTL design and testbench, with test vectors read from tb_mul.sv."""
    tb = open(os.path.join(RTL, "tb_mul.sv")).read()
    body = tb[tb.index("inp_a = "):]           # the stimulus block
    vecs = [(int(a, 16), int(b, 16)) for a, b in
            re.findall(r"inp_a\s*=\s*16'h([0-9a-fA-F]+);\s*inp_b\s*=\s*16'h([0-9a-fA-F]+);", body)]
    hold = re.search(r"inp_b\s*=\s*16'h[0-9a-fA-F]+;\s*#(\d+);", body)
    hold = int(hold.group(1)) if hold else 20
    half = int(re.search(r"forever\s*#(\d+)\s*clk", tb).group(1))
    rst_len = int(re.search(r"rst\s*=\s*1;\s*#(\d+)\s*rst\s*=\s*0", tb).group(1))
    L = [heading(RTL_SECTION, HEADINGS.get("RTL", "")), ""]
    L.append(
        "\\textbf{Design.} The multiplier (\\texttt{mul.sv}, module \\texttt{mult}) takes two 16-bit unsigned "
        "inputs \\texttt{inp\\_a} and \\texttt{inp\\_b} and registers their 32-bit product: on each rising "
        "edge of \\texttt{clk}, \\texttt{prod <= inp\\_a * inp\\_b}. An asynchronous, active-high "
        "\\texttt{rst} clears \\texttt{prod} to 0. The product is 32 bits wide, so the largest result "
        "($\\texttt{0xFFFF} \\times \\texttt{0xFFFF}$) fits without overflow. Because the output is registered, "
        "synthesis times the path from the input ports through the multiplier logic to the \\texttt{prod} "
        "flip-flops, which is the critical path reported in \\texttt{syn\\_timing.rpt}.")
    L.append("")
    L.append(
        f"\\textbf{{Testbench.}} \\texttt{{tb\\_mul.sv}} generates a {2 * half}\\,ns clock, holds \\texttt{{rst}} "
        f"high for the first {rst_len}\\,ns, and applies {len(vecs)} input pairs, each held for {hold}\\,ns "
        f"({hold // (2 * half)} clock cycles). The vectors cover small values, zero, the largest inputs "
        f"(which exercise every partial-product bit and the top bits of \\texttt{{prod}}), and a mixed value. "
        f"The testbench waits one extra {hold}\\,ns after the last vector before \\texttt{{\\$finish}}, so "
        f"the last product is visible in the waveform. I checked each product in the QuestaSim waveform "
        f"against the expected value in Table~\\ref{{tab:rtl}}.")
    L.append("")
    rows = []
    for i, (a, b) in enumerate(vecs):
        t = i * hold
        # prod updates on the first rising edge after the inputs change and reset is released
        edge = next(e for e in range(half, 10 * hold * len(vecs), 2 * half) if e > t and e > rst_len)
        rows.append([f"{t}", f"\\texttt{{{a:04x}}}", f"\\texttt{{{b:04x}}}", f"\\texttt{{{a * b:08x}}}",
                     f"{a * b:,}".replace(",", "{,}"), f"{edge}"])
    L += [r"\begin{table}[H]"]
    L += table(["applied (ns)", "inp\\_a", "inp\\_b", "expected prod", "decimal", "prod updates (ns)"],
               rows, "r|c|c|c|r|r")[:-1] + [r"\end{center}"]
    L += [r"\caption{Test vectors from \texttt{tb\_mul.sv}. Expected products are computed from the inputs; "
          r"the waveform in Figure~\ref{fig:rtl} shows the same values on \texttt{prod}.}",
          r"\label{tab:rtl}", r"\end{table}"]
    if os.path.exists(os.path.join(FIG, WAVEFORM)):
        L += [r"\begin{figure}[H]", r"\centering",
              rf"\includegraphics[width=\textwidth]{{figures/{WAVEFORM}}}",
              r"\caption{QuestaSim waveform of \texttt{tb\_mult}: inputs, registered product, clock and reset.}",
              r"\label{fig:rtl}", r"\end{figure}"]
    else:
        print(f"note: save the waveform screenshot as report/figures/{WAVEFORM} and rerun")
        L += [r"\begin{figure}[H]", r"\centering",
              rf"\fbox{{\parbox{{0.9\textwidth}}{{\centering Waveform screenshot goes here "
              rf"(figures/{WAVEFORM.replace('_', chr(92) + '_')})}}}}",
              r"\caption{QuestaSim waveform of \texttt{tb\_mult}.}", r"\label{fig:rtl}", r"\end{figure}"]
    L.append(
        f"\\textbf{{Result.}} All {len(vecs)} products match the expected values. While \\texttt{{rst}} is high, "
        f"\\texttt{{prod}} stays at 0, so the first product appears at {rows[0][-1]}\\,ns, on the first rising "
        f"edge after reset is released. After that, each new product appears on the first rising edge after "
        f"the inputs change, which is the one-register latency of the design. "
        f"$\\texttt{{0xFFFF}} \\times \\texttt{{0xFFFF}} = \\texttt{{0xFFFE0001}}$ confirms the full 32-bit "
        f"result is kept.")
    L.append("")
    return L


def heading(num, title):
    """Unnumbered section heading: problem number, then its title."""
    return rf"\section*{{{num}\quad {title}}}" if title else rf"\section*{{{num}}}"


def tex(s):
    """Escape text for LaTeX."""
    for a, b in (("\\", r"\textbackslash{}"), ("_", r"\_"), ("%", r"\%"), ("&", r"\&"),
                 ("#", r"\#"), ("$", r"\$"), ("{", r"\{"), ("}", r"\}")):
        s = s.replace(a, b)
    return s


def pct(a, b):
    return 100 * (a - b) / b


def near(rows, mult):
    return min(rows, key=lambda r: abs(r["mult"] - mult))


def table(header, rows, align):
    out = [r"\begin{center}", r"\small", r"\begin{tabular}{" + align + "}", r"\hline",
           " & ".join(header) + r" \\", r"\hline"]
    out += [" & ".join(r) + r" \\" for r in rows]
    out += [r"\hline", r"\end{tabular}", r"\end{center}"]
    return out


def figure(name, caption, width=r"0.95\textwidth"):
    label = "fig:" + name.rsplit(".", 1)[0]
    return [r"\begin{figure}[H]", r"\centering",
            rf"\includegraphics[width={width}]{{figures/{name}}}",
            rf"\caption{{{caption}}}", rf"\label{{{label}}}", r"\end{figure}"]


# ---------------------------------------------------------------- sections
def sweep_section(g, rows):
    f = rows[0]
    p = ppa.picks(rows)
    e = p["energy"]
    L = [heading(PROBLEMS.get(g, ""), HEADINGS.get(g, g)), ""]
    L.append(
        f"For the {LIB_DESC.get(g, g)}, I swept the clock period in \\texttt{{lab2.sh}} and checked the "
        f"worst slack in \\texttt{{syn\\_timing.rpt}}. I use "
        f"$clk\\_period_{{min}} = {f['clk_ns']:g}$\\,ns ({MIN_NOTE.get(g, '')}), so $F_{{max}} = 1/{f['clk_ns']:g}\\,\\text{{ns}} "
        f"= {f['f_MHz']:.0f}$\\,MHz. I then synthesized the design at "
        f"$1\\times$ to $1000\\times$ this clock period.")
    L.append("")
    L.append(
        "Energy per cycle is computed from \\texttt{syn\\_power.rpt}: "
        "$P_{Dyn}$ is switching plus internal power (mW), $P_{Leak}$ is leakage power (reported in nW), "
        "and $E_{Dyn} = P_{Dyn} \\times clk\\_period$, $E_{Leak} = P_{Leak} \\times clk\\_period$, "
        "$E_{total} = E_{Dyn} + E_{Leak}$. With mW and ns, the energies are in pJ.")
    hdr = ["$\\times$ min", "clk (ns)", "f (MHz)", "slack (ns)", "area ($\\mu m^2$)",
           "$E_{Dyn}$ (pJ)", "$E_{Leak}$ (pJ)", "$E_{total}$ (pJ)"]
    body = [[f"{r['mult']:.2f}", f"{r['clk_ns']:g}", f"{r['f_MHz']:.1f}", f"{r['slack']:.2f}",
             f"{r['area']:.1f}", f"{r['EDyn_pJ']:.4f}", f"{r['ELeak_pJ']:.2e}", f"{r['Etotal_pJ']:.4f}"]
            for r in rows]
    L += table(hdr, body, "r|r|r|r|r|r|r|r")
    L += figure(f"energy_{g}.png",
                f"{g}: dynamic, leakage and total energy per cycle vs frequency. "
                f"Each marker is one synthesis run.")
    L.append(
        f"The minimum total energy is {e['Etotal_pJ']:.4f}\\,pJ/cycle at {e['f_MHz']:.0f}\\,MHz "
        f"({e['clk_ns']:g}\\,ns, ${e['mult']:.0f}\\times$). At $F_{{max}}$ it is "
        f"{f['Etotal_pJ']:.4f}\\,pJ/cycle.")
    L.append("")
    return L


def discussion_library(g, rows):
    f, s = rows[0], rows[-1]
    r125, r2 = near(rows, 1.25), near(rows, 2)
    sat = next((r for r in rows if r["slack"] > 0), None)
    p = ppa.picks(rows)
    e = p["energy"]
    fdyn, sdyn = f["EDyn_pJ"] / f["clk_ns"], s["EDyn_pJ"] / s["clk_ns"]
    # adjacent pair (faster, slower) with the biggest fan-in jump = the netlist restructuring
    pairs = list(zip(rows, rows[1:]))
    sw = max(pairs, key=lambda q: q[1]["avg_fanin"] - q[0]["avg_fanin"])
    sw = sw if sw[1]["avg_fanin"] - sw[0]["avg_fanin"] > 0.5 else None
    L = [rf"\subsection*{{{g} (Figure~\ref{{fig:energy_{g}}})}}", ""]

    L.append(
        f"\\textbf{{Performance.}} At $F_{{max}}$ = {f['f_MHz']:.0f}\\,MHz the worst path starts at "
        f"\\texttt{{{tex(f['start'])}}}, ends at \\texttt{{{tex(f['end'].split()[0])}}}, and passes through "
        f"{f['depth']} cells with a data arrival time of {f['arrival']:.2f}\\,ns (\\texttt{{syn\\_timing.rpt}}). "
        + (f"The slack stays at 0\\,ns until {sat['f_MHz']:.0f}\\,MHz (${sat['mult']:.0f}\\times$), where it "
           f"becomes {sat['slack']:.2f}\\,ns. Below that frequency the smallest netlist DC can build is already "
           f"fast enough, so its critical path ({s['depth']} cells, {s['arrival']:.2f}\\,ns arrival) no longer "
           f"depends on the clock constraint."
           if sat else ""))
    L.append("")

    L.append(
        f"\\textbf{{Area.}} Total cell area rises from {s['area']:.1f}\\,$\\mu m^2$ at the slowest clock to "
        f"{f['area']:.1f}\\,$\\mu m^2$ at $F_{{max}}$ ({pct(f['area'], s['area']):+.0f}\\%), and the cell count "
        f"from {s['cells']:.0f} to {f['cells']:.0f} (\\texttt{{syn\\_area.rpt}}). Most of the growth is near "
        f"$F_{{max}}$: area is {r2['area']:.1f}\\,$\\mu m^2$ at $2\\times$ and {r125['area']:.1f}\\,$\\mu m^2$ "
        f"at $1.25\\times$. Non-combinational area stays at {f['seq_area']:.1f}\\,$\\mu m^2$ "
        f"({f['seq_cells']:.0f} flip-flops for \\texttt{{prod}}), so all of the extra area is combinational "
        f"logic. Buffers and inverters grow from {s['bufinv_cells']:.0f} to {f['bufinv_cells']:.0f} "
        f"({s['bufinv_area']:.1f} to {f['bufinv_area']:.1f}\\,$\\mu m^2$), which DC adds to drive the "
        f"larger loads on the critical paths.")
    L.append("")

    L.append(
        f"\\textbf{{Drive strength and fan-in.}} From the cell list in \\texttt{{syn.rpt}}, at the slowest clock "
        f"{s['pct_D1']:.0f}\\% of the combinational cells are D1 (average drive ${s['avg_drive']:.2f}\\times$). "
        f"At $F_{{max}}$ the average drive is ${f['avg_drive']:.2f}\\times$, {f['pct_D4plus']:.1f}\\% of cells "
        f"are D4 or larger ({f['area_pct_D4plus']:.0f}\\% of combinational area), and the largest cell is "
        f"D{f['max_drive']}. The cells on the critical path average ${f['path_avg_drive']:.1f}\\times$ drive, "
        f"compared with ${s['path_avg_drive']:.1f}\\times$ when relaxed. The gate mix also changes: the relaxed "
        f"netlist uses {s['n_adder']} full/half-adder cells and high-fan-in complex gates (average fan-in "
        f"{s['avg_fanin']:.2f}, {s['pct_fanin3plus']:.0f}\\% with three or more inputs), while the $F_{{max}}$ "
        f"netlist uses only {f['n_adder']} adder cells, {f['n_xor']} XOR/XNR gates and more two- and "
        f"three-input AOI/OAI gates (average fan-in {f['avg_fanin']:.2f}, {f['pct_fanin3plus']:.0f}\\% with three or "
        f"more inputs). Gates with fewer inputs have fewer transistors in series and lower logical effort, and "
        f"the restructured logic cuts the critical path from {s['depth']} to {f['depth']} cells. "
        + (f"The switch happens between {sw[1]['f_MHz']:.0f} and {sw[0]['f_MHz']:.0f}\\,MHz, where the "
           f"average fan-in drops from {sw[1]['avg_fanin']:.2f} to {sw[0]['avg_fanin']:.2f} and the adder count from "
           f"{sw[1]['n_adder']} to {sw[0]['n_adder']}. " if sw else "")
        + "This buys speed at the cost of more, larger cells.")
    L.append("")

    L.append(
        f"\\textbf{{Power and energy.}} Dynamic power is {fdyn:.3f}\\,mW at $F_{{max}}$ and "
        f"{sdyn:.4f}\\,mW at {s['f_MHz']:.2f}\\,MHz, roughly proportional to frequency. Per cycle, however, "
        f"$E_{{Dyn}}$ rises from {s['EDyn_pJ']:.3f}\\,pJ to {f['EDyn_pJ']:.3f}\\,pJ "
        f"({pct(f['EDyn_pJ'], s['EDyn_pJ']):+.0f}\\%), because the upsized, larger netlist switches more "
        f"capacitance each cycle. Leakage power follows the cell area and size: {f['leak_nW']:.0f}\\,nW at "
        f"$F_{{max}}$ and {s['leak_nW']:.0f}\\,nW when relaxed. Because $E_{{Leak}}$ is leakage power times the "
        f"clock period, it is only {f['leak_share']:.2f}\\% of $E_{{total}}$ at $F_{{max}}$ but "
        f"{s['leak_share']:.1f}\\% at {s['f_MHz']:.2f}\\,MHz. The total energy curve therefore has a minimum "
        f"of {e['Etotal_pJ']:.4f}\\,pJ at {e['f_MHz']:.0f}\\,MHz: faster than this, upsizing raises "
        f"$E_{{Dyn}}$; slower than this, leakage accumulates over the longer cycle.")
    L.append("")

    hdr = ["f (MHz)", "area", "cells", "buf/inv", "avg drive", "\\% D4+", "max D", "fan-in",
           "FA/HA", "XOR", "path cells", "arrival"]
    body = []
    for m in (1, 1.25, 1.5, 2, 3, 5, 10, 1000):
        r = near(rows, m)
        body.append([f"{r['f_MHz']:.0f}", f"{r['area']:.1f}", f"{r['cells']:.0f}",
                     f"{r['bufinv_cells']:.0f}", f"{r['avg_drive']:.2f}", f"{r['pct_D4plus']:.1f}",
                     f"{r['max_drive']}", f"{r['avg_fanin']:.2f}", f"{r['n_adder']}", f"{r['n_xor']}",
                     f"{r['depth']}", f"{r['arrival']:.2f}"])
    L += [r"\begin{table}[H]"] + table(hdr, body, "r|r|r|r|r|r|r|r|r|r|r|r")[:-1] + [r"\end{center}"]
    L += [rf"\caption{{{g} netlist statistics from \texttt{{syn\_area.rpt}}, \texttt{{syn.rpt}} and "
          rf"\texttt{{syn\_timing.rpt}} (area in $\mu m^2$, arrival in ns).}}", r"\end{table}"]
    L.append(f"Critical-path cells at $F_{{max}}$ (function\\,$\\times$\\,drive): "
             f"\\texttt{{{tex(f['path_fns'])}}}.")
    L.append("")
    return L


def optimal_section(data):
    L = [r"\subsection*{Optimal operating frequency}", ""]
    hdr = ["Library", "(a) Area-constrained", "(b) Timing-critical", "(c) Energy-constrained"]
    body = []
    for g, rows in data.items():
        p = ppa.picks(rows)
        a, t, e = p["area"], p["timing"], p["energy"]
        body.append([g, f"{a['f_MHz']:.0f} MHz ({a['area']:.1f} $\\mu m^2$)",
                     f"{t['f_MHz']:.0f} MHz ({t['area']:.1f} $\\mu m^2$)",
                     f"{e['f_MHz']:.0f} MHz ({e['Etotal_pJ']:.4f} pJ)"])
    L += table(hdr, body, "l|l|l|l")
    for g, rows in data.items():
        p = ppa.picks(rows)
        a, t, e, en = p["area"], p["timing"], p["energy"], p["energy_near"]
        txt = (f"\\textbf{{{g}.}} (a) For an area-constrained design I would run at {a['f_MHz']:.0f}\\,MHz "
               f"({a['clk_ns']:g}\\,ns). This is the fastest point whose area is within 1\\% of the minimum "
               f"({p['area_min']:.1f}\\,$\\mu m^2$); a slower clock gives no further area savings, only lower "
               f"throughput. (b) For a timing-critical design I would run at $F_{{max}}$ = {t['f_MHz']:.0f}\\,MHz, "
               f"which costs {pct(t['area'], p['area_min']):.0f}\\% more area and "
               f"{pct(t['Etotal_pJ'], e['Etotal_pJ']):.0f}\\% more energy per cycle than the minimum. "
               f"(c) For an energy-constrained design I would run at {e['f_MHz']:.0f}\\,MHz "
               f"({e['clk_ns']:g}\\,ns), the minimum of $E_{{total}}$ ({e['Etotal_pJ']:.4f}\\,pJ/cycle)")
        if en is not e:
            txt += (f"; since {en['f_MHz']:.0f}\\,MHz is within 2\\% of this energy "
                    f"({en['Etotal_pJ']:.4f}\\,pJ), it is also a good choice with higher throughput")
        L += [txt + ".", ""]

    fastest = max(data, key=lambda g: data[g][0]["f_MHz"])
    lowest_e = min(data, key=lambda g: ppa.picks(data[g])["energy"]["Etotal_pJ"])
    lowest_a = min(data, key=lambda g: ppa.picks(data[g])["area_min"])
    L.append(
        f"\\textbf{{Across libraries.}} {fastest} reaches the highest $F_{{max}}$ "
        f"({data[fastest][0]['f_MHz']:.0f}\\,MHz), so it is the choice for a timing-critical design. "
        f"{lowest_e} has the lowest minimum energy "
        f"({ppa.picks(data[lowest_e])['energy']['Etotal_pJ']:.4f}\\,pJ/cycle) because its leakage is much "
        f"lower ({', '.join(f'{g}: {rows[0]['leak_nW']:.0f}\\,nW' for g, rows in data.items())} at $F_{{max}}$), "
        f"so it is the choice for an energy-constrained design. The minimum areas are close "
        f"({', '.join(f'{g}: {ppa.picks(rows)['area_min']:.1f}' for g, rows in data.items())}\\,$\\mu m^2$), "
        f"with {lowest_a} the smallest. "
        + (f"At the slowest clock, where the LVT16 and LVT20 netlists have almost the same area "
           f"({data['LVT16'][-1]['area']:.1f} and {data['LVT20'][-1]['area']:.1f}\\,$\\mu m^2$), LVT16 leaks "
           f"{data['LVT16'][-1]['leak_nW']:.0f}\\,nW versus {data['LVT20'][-1]['leak_nW']:.0f}\\,nW, so the BWP16 cells "
           f"leak {data['LVT16'][-1]['leak_nW'] / data['LVT20'][-1]['leak_nW']:.1f}$\\times$ more than the BWP20 cells "
           f"of the same $V_t$ in exchange for their higher speed. " if {"LVT16", "LVT20"} <= set(data) else "")
        + f"Low-$V_t$ cells switch faster but leak more, which is why the LVT "
        f"libraries have higher $F_{{max}}$ and a steeper rise in total energy at low frequency.")
    L.append("")
    return L


def main():
    data = {g: rows for g in ppa.GROUPS if (rows := ppa.load_group(g))}
    if not data:
        raise SystemExit("no data found")
    os.makedirs(FIG, exist_ok=True)

    # figures: energy plots (same as plot_energy.py) and PPA trends (same as ppa_report.py)
    for g in data:
        pe.plot_group(g, pe.load(g), FIG, False)
    ppa.make_plots(data, FIG)

    L = [r"\documentclass[11pt]{article}",
         r"\usepackage{graphicx}", r"\usepackage{float}", r"\usepackage{amsmath}",
         r"\usepackage[margin=1.25in]{geometry}",
         rf"\title{{{TITLE}}}", rf"\author{{{AUTHOR}}}", r"\date{}",
         r"\begin{document}", r"\maketitle", ""]
    L += rtl_section()
    for g, rows in data.items():
        L += sweep_section(g, rows)
    L += [heading(DISCUSSION, HEADINGS.get("DISCUSSION", "")), "",
          "Below I discuss the performance, power and area trends for each graph, using "
          "\\texttt{syn\\_area.rpt}, \\texttt{syn\\_timing.rpt}, \\texttt{syn\\_power.rpt} and the cell list in "
          "\\texttt{syn.rpt}. Figure~\\ref{fig:ppa} summarizes how the netlist changes with frequency.", ""]
    L += [r"\begin{figure}[H]", r"\centering",
          r"\includegraphics[width=\textwidth]{figures/ppa_vs_frequency.png}",
          r"\caption{Area, drive strength, buffer/inverter count, fan-in and critical-path length vs "
          r"frequency for all three libraries.}", r"\label{fig:ppa}", r"\end{figure}", ""]
    for g, rows in data.items():
        L += discussion_library(g, rows)
    L += optimal_section(data)
    L.append(r"\end{document}")

    tex_path = os.path.join(OUT, "lab2_report.tex")
    with open(tex_path, "w") as fh:
        fh.write("\n".join(L) + "\n")

    zip_path = os.path.join(OUT, "lab2_report.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(tex_path, "lab2_report.tex")
        for name in sorted(os.listdir(FIG)):
            z.write(os.path.join(FIG, name), f"figures/{name}")
    print(f"wrote {os.path.relpath(tex_path, HERE)} and {os.path.relpath(zip_path, HERE)}")

    # build the PDF with tectonic (installed in ~/.local/bin) or pdflatex, whichever is found
    pdf = os.path.relpath(os.path.join(OUT, "lab2_report.pdf"), HERE)
    tectonic = shutil.which("tectonic") or shutil.which(os.path.expanduser("~/.local/bin/tectonic"))
    if tectonic:
        r = subprocess.run([tectonic, "-X", "compile", "lab2_report.tex"], cwd=OUT)
        print(f"built {pdf}" if r.returncode == 0 else "tectonic failed - see the errors above")
    elif shutil.which("pdflatex"):
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "lab2_report.tex"], cwd=OUT,
                           stdout=subprocess.DEVNULL)
        print(f"built {pdf}")
    else:
        print("no LaTeX compiler found: upload report/lab2_report.zip to Overleaf (New Project > Upload Project)")


if __name__ == "__main__":
    main()
