#!/usr/bin/env python3
"""Cross-check sheet for the Lab 2 report (for your own checking, not part of the PDF).

For each library and each design point cited in the discussion, lists the value used in
the report and a link to the exact line in the DC report it came from. Values that are
counted from the cell list (drive strength, fan-in, adders) have no single line, so the
sheet gives a grep command to recount them.

Output: report/sources.md  (open in VS Code; Ctrl+click a link to jump to that line,
or right-click the tab > Open Preview for clickable links)

Usage:  python3.12 check_sources.py
"""
import os

import ppa_report as ppa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "report", "sources.md")
# design points cited in the discussion: Fmax, the netlist table rows, and the slowest run
MULTS = [1, 1.25, 1.5, 2, 3, 5, 10, 1000]


def find(path, test, start=0):
    """(line_number, text) of the first line after `start` for which test(line) is true."""
    with open(path) as f:
        for n, line in enumerate(f, 1):
            if n > start and test(line):
                return n, line.rstrip()
    return None, ""


def link(path, n, label=None):
    rel = os.path.relpath(path, os.path.dirname(OUT))
    name = label or os.path.basename(path)
    return f"[{name}:{n}]({rel}#L{n})" if n else f"{name}: not found"


def point(g, r, why):
    clk = f"{r['clk_ns']:g}"
    pre = os.path.join(HERE, "reports", g, f"mult.{clk}.{g}.syn")
    area, timing, cells, power = pre + "_area.rpt", pre + "_timing.rpt", pre + ".rpt", pre + "_power.rpt"
    L = [f"### {g} @ {clk} ns ({r['mult']:g}x, {r['f_MHz']:.1f} MHz) - {why}", ""]

    L.append("**syn_area.rpt**")
    L.append("")
    for key, label, fmt in [("Number of cells", "cells", "{:.0f}"),
                            ("Number of sequential cells", "seq_cells", "{:.0f}"),
                            ("Number of buf/inv", "bufinv_cells", "{:.0f}"),
                            ("Buf/Inv area", "bufinv_area", "{:.2f}"),
                            ("Noncombinational area", "seq_area", "{:.2f}"),
                            ("Total cell area", "area", "{:.2f}")]:
        n, _ = find(area, lambda l, k=key: l.strip().startswith(k + ":"))
        L.append(f"- {key} = **{fmt.format(r[label])}** -> {link(area, n)}")
    L.append("")

    L.append("**syn_timing.rpt** (first path = worst path)")
    L.append("")
    n1, _ = find(timing, lambda l: l.strip().startswith("Startpoint:"))
    n2, _ = find(timing, lambda l: l.strip().startswith("Endpoint:"))
    n3, _ = find(timing, lambda l: l.strip().startswith("data arrival time"))
    n4, _ = find(timing, lambda l: l.strip().startswith("slack ("))
    np, _ = find(timing, lambda l: l.strip().startswith("Point"))
    L.append(f"- Startpoint = **{r['start']}** -> {link(timing, n1)}")
    L.append(f"- Endpoint = **{r['end'].split()[0]}** -> {link(timing, n2)}")
    L.append(f"- Path cells = **{r['depth']}** (cell lines between {link(timing, np, 'Point')} and "
             f"{link(timing, n3, 'data arrival')}, not counting the endpoint flop's D pin)")
    L.append(f"- Data arrival = **{r['arrival']:.2f} ns** -> {link(timing, n3)}")
    L.append(f"- Slack = **{r['slack']:.2f} ns** -> {link(timing, n4)}")
    L.append(f"- Path cells (function x drive), avg drive x{r['path_avg_drive']:.1f}: `{r['path_fns']}`")
    L.append("")

    L.append("**syn_power.rpt**")
    L.append("")
    n, _ = find(power, lambda l: l.split()[:1] == ["mult"] and len(l.split()) >= 5)
    L.append(f"- Switch = **{r['switch_mW']:g} mW**, Int = **{r['int_mW']:g} mW**, "
             f"Leak = **{r['leak_nW']:g} nW** -> {link(power, n)}")
    L.append(f"- E_dyn = (Switch + Int) x {clk} = **{r['EDyn_pJ']:.4f} pJ**, "
             f"E_leak = Leak/1e6 x {clk} = **{r['ELeak_pJ']:.3e} pJ**, "
             f"E_total = **{r['Etotal_pJ']:.4f} pJ** ({r['leak_share']:.2f}% leakage)")
    L.append("")

    L.append("**syn.rpt** (counted from the cell list; no single line)")
    L.append("")
    n, _ = find(cells, lambda l: l.startswith("Total ") and "cells" in l)
    rel = os.path.relpath(cells, HERE)
    L.append(f"- Total cells = **{r['cells']:.0f}** -> {link(cells, n)}")
    L.append(f"- Avg drive x**{r['avg_drive']:.2f}**, D1 **{r['pct_D1']:.1f}%**, D4+ **{r['pct_D4plus']:.1f}%** "
             f"of cells ({r['area_pct_D4plus']:.1f}% of comb. area), largest **D{r['max_drive']}**")
    L.append(f"- Avg fan-in **{r['avg_fanin']:.2f}** ({r['pct_fanin3plus']:.1f}% with 3+ inputs), "
             f"FA/HA **{r['n_adder']}**, XOR/XNR **{r['n_xor']}**, complex AOI/OAI **{r['n_complex']}**, "
             f"simple NAND/NOR **{r['n_simple']}**")
    # only the report_cell section: the port section of syn.rpt also names (driving) cells
    cell_list = f"sed -n '/^Report : cell/,/^Total .* cells/p' {rel}"
    L.append(f"- Recount drive strengths of the {r['comb_cells']:.0f} combinational cells (run in `synthesis/lab2/`):")
    L.append(f"  `{cell_list} | grep -oE '[A-Z0-9]+D[0-9]+BWP' | grep -v '^DF' | sed -E 's/.*(D[0-9]+)BWP/\\1/' | sort | uniq -c`")
    L.append(f"- Recount adders: `{cell_list} | grep -cE '\\b(FA1|HA1)D[0-9]+BWP'`")
    L.append("")
    return L


def main():
    L = ["# Report cross-check sheet", "",
         "Each value below is what `lab2_report.py` puts in the report. Links go to the line in the DC report "
         "it was read from (Ctrl+click in the editor, or open the Markdown preview). Area in um^2.", ""]
    for g in ppa.GROUPS:
        rows = ppa.load_group(g)
        if not rows:
            continue
        sat = next((r for r in rows if r["slack"] > 0), None)
        emin = min(rows, key=lambda r: r["Etotal_pJ"])
        L += [f"## {g}", ""]
        L += [f"- F_max point: {rows[0]['clk_ns']:g} ns; slowest point: {rows[-1]['clk_ns']:g} ns",
              f"- First positive slack: {sat['clk_ns']:g} ns" if sat else "- Slack never positive",
              f"- Minimum E_total: {emin['Etotal_pJ']:.4f} pJ at {emin['clk_ns']:g} ns "
              f"(check against `reports/{g}/energy.csv`)", ""]
        cited = []
        for m in MULTS:
            r = ppa_near(rows, m)
            if r not in cited:
                cited.append(r)
        for r in cited:
            why = []
            if r is rows[0]:
                why.append("F_max (Performance / Drive strength / critical-path list)")
            if r is sat:
                why.append("first positive slack (Performance)")
            if r is rows[-1]:
                why.append("slowest clock ('relaxed' in the discussion)")
            if r is emin:
                why.append("minimum E_total")
            why.append("netlist table row")
            L += point(g, r, "; ".join(why))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(OUT, HERE)}")


def ppa_near(rows, m):
    return min(rows, key=lambda r: abs(r["mult"] - m))


if __name__ == "__main__":
    main()
