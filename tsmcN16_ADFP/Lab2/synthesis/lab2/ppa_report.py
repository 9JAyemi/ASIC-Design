#!/usr/bin/env python3
"""PPA report for the Lab 2 clock-period sweeps.

For every cell group and clock period in reports/<group>/, this reads
  mult.<clk>.<group>.syn_area.rpt    area, cell counts, buf/inv
  mult.<clk>.<group>.syn_timing.rpt  worst path: arrival, slack, logic depth, cells on it
  mult.<clk>.<group>.syn.rpt         full cell list: drive strength and fan-in mix
  mult.<clk>.<group>.syn_power.rpt   switching / internal / leakage power
and energy from reports/<group>/energy.csv.

It writes
  results/ppa_report.md        tables, observations and optimal-frequency picks
  results/ppa_<group>.csv      every metric per clock period
  plots/ppa_*.png              area, drive strength, fan-in, logic depth vs frequency

Usage:  python3.12 ppa_report.py [GROUP ...]   (default: SVT20 LVT20 LVT16)
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = ["SVT20", "LVT20", "LVT16"]
REF_RE = re.compile(r"^[A-Z0-9]+BWP[0-9A-Z]+$")
FLOAT_RE = re.compile(r"^-?\d+\.\d+(e[+-]?\d+)?$")

# ---------------------------------------------------------------- cell names
# TSMC N16 names look like <function>D<drive>BWP<height>P90[LVT], e.g.
# ND2D1BWP20P90 (2-input NAND, x1), OAI22D2BWP16P90LVT, FA1D1BWP20P90, CKND8BWP20P90


def split_cell(ref):
    """'OAI22D2BWP20P90' -> ('OAI22', 2)."""
    base = ref.split("BWP")[0]
    m = re.search(r"D(\d+)$", base)
    return (base[:m.start()], int(m.group(1))) if m else (base, 0)


def cell_class(fn):
    if fn.startswith("DF"):
        return "flop"
    if fn in ("INV", "CKN", "BUFF", "CKB"):
        return "buf/inv"
    if fn in ("FA1", "HA1"):
        return "adder"
    if fn.startswith(("XOR", "XNR")):
        return "xor"
    if re.match(r"^(C?K?)(ND|NR|AN|OR|IND|INR|IINR|CKND|CKNR|CKAN)\d$", fn):
        return "simple"
    return "complex"  # AOI/OAI/AO/OA/MAOI/...


def fan_in(fn):
    """Number of logic inputs of a combinational cell (None for flops)."""
    cls = cell_class(fn)
    if cls == "flop":
        return None
    if cls == "buf/inv":
        return 1
    if fn == "FA1":
        return 3
    if fn == "HA1":
        return 2
    digits = re.search(r"(\d+)$", fn)
    if not digits:
        return 1
    d = digits.group(1)
    if cls == "complex":                # AOI22 -> 4, OAI211 -> 4, MAOI222 -> 6
        return sum(int(c) for c in d)
    return int(d)                       # ND3 -> 3, XNR2 -> 2


# ---------------------------------------------------------------- parsers
def parse_area(path):
    keys = {
        "Number of cells": "cells", "Number of combinational cells": "comb_cells",
        "Number of sequential cells": "seq_cells", "Number of buf/inv": "bufinv_cells",
        "Number of references": "references", "Combinational area": "comb_area",
        "Buf/Inv area": "bufinv_area", "Noncombinational area": "seq_area",
        "Total cell area": "area",
    }
    out = {}
    for line in open(path):
        if ":" in line:
            k, v = line.split(":", 1)
            if k.strip() in keys:
                out[keys[k.strip()]] = float(v.split()[0])
    return out


def parse_timing(path):
    """Worst (first) path only."""
    out = {"start": "", "end": "", "arrival": None, "slack": None, "path_cells": []}
    in_path = False
    for line in open(path):
        s = line.strip()
        if s.startswith("Startpoint:") and not out["start"]:
            out["start"] = s.split(":", 1)[1].split("(")[0].strip()
        elif s.startswith("Endpoint:") and not out["end"]:
            out["end"] = s.split(":", 1)[1].strip()
        elif s.startswith("Point") and out["arrival"] is None:
            in_path = True
        elif s.startswith("data arrival time") and in_path:
            out["arrival"] = float(s.split()[-1])
            in_path = False
        elif in_path:
            m = re.match(r"^(\S+)/(\S+) \(([A-Z0-9]+BWP[0-9A-Z]+)\)", s)
            if m:
                out["path_cells"].append((m.group(1), m.group(2), m.group(3)))
        elif s.startswith("slack (") and out["slack"] is None:
            out["slack"] = float(s.split()[-1])
            break
    cells = out["path_cells"]
    # the endpoint flop's D pin is not a logic stage
    if cells and cells[-1][1] in ("D", "SI", "SE"):
        cells = cells[:-1]
    out["depth"] = len(cells)
    drives = [split_cell(c[2])[1] for c in cells]
    out["path_avg_drive"] = sum(drives) / len(drives) if drives else 0
    out["path_fns"] = " ".join(f"{split_cell(c[2])[0]}x{split_cell(c[2])[1]}" for c in cells)
    return out


def parse_cells(path):
    """(reference, area) for every cell in the report_cell section of syn.rpt."""
    cells, in_cells, pending = [], False, None
    for line in open(path):
        if line.startswith("Report : cell"):
            in_cells = True
            continue
        if in_cells and line.startswith("Total ") and "cells" in line:
            break
        if not in_cells:
            continue
        for tok in line.split():
            if REF_RE.match(tok):
                pending = tok
            elif pending and FLOAT_RE.match(tok):
                cells.append((pending, float(tok)))
                pending = None
    return cells


def cell_mix(cells):
    out = {}
    comb = [(split_cell(r), a) for r, a in cells if cell_class(split_cell(r)[0]) != "flop"]
    n = len(comb)
    area = sum(a for _, a in comb)
    drives = Counter(d for (_, d), _ in comb)
    out["avg_drive"] = sum(d * c for d, c in drives.items()) / n
    out["pct_D1"] = 100 * drives.get(1, 0) / n
    out["pct_D2"] = 100 * drives.get(2, 0) / n
    out["pct_D4plus"] = 100 * sum(c for d, c in drives.items() if d >= 4) / n
    out["area_pct_D4plus"] = 100 * sum(a for (_, d), a in comb if d >= 4) / area
    out["max_drive"] = max(drives)
    fis = [fan_in(fn) for (fn, _), _ in comb]
    logic = [f for f, ((fn, _), _) in zip(fis, comb) if cell_class(fn) != "buf/inv"]
    out["avg_fanin"] = sum(logic) / len(logic)
    out["pct_fanin3plus"] = 100 * sum(1 for f in logic if f >= 3) / len(logic)
    classes = Counter(cell_class(fn) for (fn, _), _ in comb)
    for k in ("adder", "xor", "complex", "simple", "buf/inv"):
        out["n_" + k.replace("/", "")] = classes.get(k, 0)
    out["top_cells"] = ", ".join(f"{r}:{c}" for r, c in Counter(r for r, _ in cells).most_common(5))
    return out


def parse_power(path):
    for line in open(path):
        p = line.split()
        if p and p[0] == "mult" and len(p) >= 5:
            return {"switch_mW": float(p[1]), "int_mW": float(p[2]), "leak_nW": float(p[3])}
    return {}


def load_group(group):
    d = os.path.join(HERE, "reports", group)
    ecsv = os.path.join(d, "energy.csv")
    if not os.path.exists(ecsv):
        print(f"skipping {group}: no {os.path.relpath(ecsv, HERE)}")
        return None
    rows = []
    for e in csv.DictReader(open(ecsv)):
        clk = e["clk_ns"]
        pre = os.path.join(d, f"mult.{clk}.{group}.syn")
        try:
            row = {"clk_ns": float(clk), "f_MHz": 1000.0 / float(clk)}
            row.update({k: float(v) for k, v in e.items() if k != "clk_ns"})
            row.update(parse_area(pre + "_area.rpt"))
            row.update(parse_timing(pre + "_timing.rpt"))
            row.update(cell_mix(parse_cells(pre + ".rpt")))
            row.update(parse_power(pre + "_power.rpt"))
        except FileNotFoundError as err:
            print(f"  {group} {clk}: missing {os.path.basename(err.filename)}, skipped")
            continue
        rows.append(row)
    rows.sort(key=lambda r: r["clk_ns"])
    clk_min = rows[0]["clk_ns"]
    for r in rows:
        r["mult"] = r["clk_ns"] / clk_min
        r["leak_share"] = 100 * r["ELeak_pJ"] / r["Etotal_pJ"]
    print(f"{group}: {len(rows)} design points")
    return rows


# ---------------------------------------------------------------- analysis
def picks(rows):
    """Optimal operating points for the three design scenarios."""
    fmax = rows[0]
    amin = min(r["area"] for r in rows)
    # area-constrained: fastest point whose area is within 1% of the minimum
    area_pt = min((r for r in rows if r["area"] <= 1.01 * amin), key=lambda r: r["clk_ns"])
    emin = min(rows, key=lambda r: r["Etotal_pJ"])
    # energy-constrained: also the fastest point within 2% of the minimum energy
    e_near = min((r for r in rows if r["Etotal_pJ"] <= 1.02 * emin["Etotal_pJ"]), key=lambda r: r["clk_ns"])
    return {"timing": fmax, "area": area_pt, "area_min": amin, "energy": emin, "energy_near": e_near}


def pct(a, b):
    return 100 * (a - b) / b


def observations(group, rows):
    f, s = rows[0], rows[-1]           # fastest (Fmax) and slowest (1000x)
    mid = min(rows, key=lambda r: abs(r["mult"] - 2))
    sat = next(r for r in rows if r["slack"] and r["slack"] > 0) if any(r["slack"] > 0 for r in rows) else None
    L = []
    L.append(f"- **Area:** {f['area']:.1f} um^2 at Fmax ({f['f_MHz']:.0f} MHz) vs {s['area']:.1f} um^2 "
             f"at {s['f_MHz']:.2f} MHz ({pct(f['area'], s['area']):+.1f}%). Cells {f['cells']:.0f} vs "
             f"{s['cells']:.0f}; buf/inv {f['bufinv_cells']:.0f} vs {s['bufinv_cells']:.0f} "
             f"(buf/inv area {f['bufinv_area']:.1f} vs {s['bufinv_area']:.1f}). "
             f"Sequential area stays {f['seq_area']:.1f} um^2 (32 output flops) - all the change is combinational.")
    L.append(f"- **Drive strength:** average combinational drive x{f['avg_drive']:.2f} at Fmax vs "
             f"x{s['avg_drive']:.2f} when relaxed; D4+ cells {f['pct_D4plus']:.1f}% vs {s['pct_D4plus']:.1f}% "
             f"of cells ({f['area_pct_D4plus']:.1f}% vs {s['area_pct_D4plus']:.1f}% of comb. area); "
             f"largest cell x{f['max_drive']} vs x{s['max_drive']}; D1 cells {f['pct_D1']:.1f}% vs {s['pct_D1']:.1f}%.")
    L.append(f"- **Fan-in / gate choice:** average logic fan-in {f['avg_fanin']:.2f} vs {s['avg_fanin']:.2f}; "
             f"cells with 3+ inputs {f['pct_fanin3plus']:.1f}% vs {s['pct_fanin3plus']:.1f}%. "
             f"Adders (FA/HA) {f['n_adder']} vs {s['n_adder']}, XOR/XNR {f['n_xor']} vs {s['n_xor']}, "
             f"complex AOI/OAI {f['n_complex']} vs {s['n_complex']}, simple NAND/NOR {f['n_simple']} vs {s['n_simple']}.")
    L.append(f"- **Critical path:** at Fmax, {f['depth']} stages, arrival {f['arrival']:.2f} ns, "
             f"avg drive x{f['path_avg_drive']:.1f} on the path ({f['start']} -> {f['end'].split()[0]}); "
             f"relaxed: {s['depth']} stages, arrival {s['arrival']:.2f} ns, avg drive x{s['path_avg_drive']:.1f}.")
    if sat:
        L.append(f"- **Saturation:** slack first becomes positive at {sat['clk_ns']:g} ns ({sat['mult']:.0f}x, "
                 f"{sat['f_MHz']:.0f} MHz), arrival {sat['arrival']:.2f} ns: DC stops optimizing for speed and "
                 f"the netlist (area {sat['area']:.1f}) barely changes for slower clocks.")
    L.append(f"- **Power/energy:** P_dyn {f['EDyn_pJ']/f['clk_ns']:.3f} mW at Fmax -> {s['EDyn_pJ']/s['clk_ns']:.4f} mW; "
             f"E_dyn {f['EDyn_pJ']:.3f} -> {mid['EDyn_pJ']:.3f} (2x) -> {s['EDyn_pJ']:.3f} pJ/cycle "
             f"(fewer, smaller cells switch less capacitance). Leakage power {f['leak_nW']:.0f} -> {s['leak_nW']:.0f} nW "
             f"tracks area, but E_leak grows with the period: {f['leak_share']:.2f}% of E_total at Fmax, "
             f"{s['leak_share']:.1f}% at 1000x.")
    return L


# ---------------------------------------------------------------- output
COLS = [("mult", "x clk_min", "{:.2f}"), ("clk_ns", "clk (ns)", "{:g}"), ("f_MHz", "f (MHz)", "{:.1f}"),
        ("slack", "slack", "{:.2f}"), ("area", "area (um^2)", "{:.1f}"), ("cells", "cells", "{:.0f}"),
        ("bufinv_cells", "buf/inv", "{:.0f}"), ("avg_drive", "avg drive", "{:.2f}"),
        ("pct_D4plus", "% D4+", "{:.1f}"), ("avg_fanin", "avg fan-in", "{:.2f}"),
        ("n_adder", "FA/HA", "{}"), ("depth", "path stages", "{}"), ("arrival", "arrival (ns)", "{:.2f}"),
        ("EDyn_pJ", "E_dyn (pJ)", "{:.4f}"), ("ELeak_pJ", "E_leak (pJ)", "{:.2e}"),
        ("Etotal_pJ", "E_total (pJ)", "{:.4f}"), ("leak_share", "leak %", "{:.2f}")]


def md_table(rows):
    out = ["| " + " | ".join(h for _, h, _ in COLS) + " |", "|" + "---|" * len(COLS)]
    for r in rows:
        out.append("| " + " | ".join(fmt.format(r[k]) for k, _, fmt in COLS) + " |")
    return out


def write_csv(group, rows, path):
    keys = [k for k in rows[0] if k != "path_cells"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def make_plots(data, out_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not found - skipping plots (run with python3.12)")
        return []
    colors = {"SVT20": "#4285F4", "LVT20": "#DB4437", "LVT16": "#0F9D58"}
    specs = [("area", "Cell area (um^2)"), ("avg_drive", "Avg drive strength (x)"),
             ("pct_D4plus", "Cells with drive >= x4 (%)"), ("bufinv_cells", "Buffer/inverter count"),
             ("avg_fanin", "Avg logic fan-in"), ("depth", "Critical-path logic stages")]
    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    for ax, (k, label) in zip(axes.flat, specs):
        for g, rows in data.items():
            ax.plot([r["f_MHz"] for r in rows], [r[k] for r in rows], "-o", ms=4,
                    color=colors.get(g), label=g)
        ax.set_xlabel("Frequency (MHz)", fontweight="bold")
        ax.set_ylabel(label, fontweight="bold")
        ax.set_title(f"{label} vs frequency", loc="left", color="#5f6368", fontweight="bold")
        ax.set_xlim(left=0)
        ax.grid(True, color="#dddddd")
        ax.legend(frameon=False)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    path = os.path.join(out_dir, "ppa_vs_frequency.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return [path]


def main():
    groups = sys.argv[1:] or GROUPS
    data = {g: rows for g in groups if (rows := load_group(g))}
    if not data:
        sys.exit("no data found")
    res = os.path.join(HERE, "results")
    plots = os.path.join(HERE, "plots")
    os.makedirs(res, exist_ok=True)
    os.makedirs(plots, exist_ok=True)

    md = ["# Lab 2 PPA report (mult, 16-bit multiplier)", "",
          "Generated by `ppa_report.py` from `reports/<group>/mult.<clk>.<group>.syn{_area,_timing,_power,}.rpt` "
          "and `energy.csv`. Area in um^2, time in ns, energy in pJ/cycle. Drive = the `D<n>` in the cell name; "
          "fan-in counts logic inputs (buf/inv excluded, flops excluded). Critical path = worst path in syn_timing.rpt.", ""]

    md += ["## Optimal operating frequency per scenario", "",
           "| Group | (a) Area-constrained | (b) Timing-critical | (c) Energy-constrained |", "|---|---|---|---|"]
    all_picks = {}
    for g, rows in data.items():
        p = picks(rows)
        all_picks[g] = p
        a, t, e, en = p["area"], p["timing"], p["energy"], p["energy_near"]
        e_txt = f"{e['f_MHz']:.0f} MHz ({e['clk_ns']:g} ns, {e['mult']:.0f}x): {e['Etotal_pJ']:.4f} pJ"
        if en is not e:
            e_txt += f"; within 2% up to {en['f_MHz']:.0f} MHz ({en['Etotal_pJ']:.4f} pJ)"
        md.append(f"| {g} | {a['f_MHz']:.0f} MHz ({a['clk_ns']:g} ns, {a['mult']:.1f}x): {a['area']:.1f} um^2 "
                  f"(min {p['area_min']:.1f}) | {t['f_MHz']:.0f} MHz ({t['clk_ns']:g} ns): Fmax, "
                  f"{t['area']:.1f} um^2, {t['Etotal_pJ']:.3f} pJ | {e_txt} |")
    md += ["",
           "- (a) Area: the fastest point whose area is within 1% of the smallest area in the sweep. Below this frequency "
           "the netlist no longer shrinks, so running slower buys no area.",
           "- (b) Timing: Fmax = 1/clk_period_min, the fastest point with slack >= 0. It costs the most area and "
           "energy per operation.",
           "- (c) Energy: the point with the lowest E_total per cycle. Faster points spend more on upsized cells; "
           "slower points spend more on leakage.", ""]

    md += ["## Cross-library comparison", "",
           "| Group | Fmax (MHz) | area @ Fmax | E_total @ Fmax | min area | min E_total @ f | leak nW @ Fmax | leak nW relaxed |",
           "|---|---|---|---|---|---|---|---|"]
    for g, rows in data.items():
        p = all_picks[g]
        md.append(f"| {g} | {rows[0]['f_MHz']:.0f} | {rows[0]['area']:.1f} | {rows[0]['Etotal_pJ']:.3f} | "
                  f"{p['area_min']:.1f} | {p['energy']['Etotal_pJ']:.4f} @ {p['energy']['f_MHz']:.0f} | "
                  f"{rows[0]['leak_nW']:.0f} | {rows[-1]['leak_nW']:.0f} |")
    md.append("")

    for g, rows in data.items():
        md += [f"## {g}", "", "### Observations (numbers to cite)", ""] + observations(g, rows)
        md += ["", "### Per design point", ""] + md_table(rows)
        md += ["", "### Critical path cells (function x drive), fastest vs slowest", "",
               f"- {rows[0]['clk_ns']:g} ns: {rows[0]['path_fns']}",
               f"- {rows[-1]['clk_ns']:g} ns: {rows[-1]['path_fns']}", "",
               "### Most used cells, fastest vs slowest", "",
               f"- {rows[0]['clk_ns']:g} ns: {rows[0]['top_cells']}",
               f"- {rows[-1]['clk_ns']:g} ns: {rows[-1]['top_cells']}", ""]
        write_csv(g, rows, os.path.join(res, f"ppa_{g}.csv"))

    for p in make_plots(data, plots):
        md += ["## Plot", "", f"![PPA vs frequency](../plots/{os.path.basename(p)})", ""]

    out = os.path.join(res, "ppa_report.md")
    with open(out, "w") as f:
        f.write("\n".join(md) + "\n")
    print(f"wrote {os.path.relpath(out, HERE)}, results/ppa_<group>.csv, plots/ppa_vs_frequency.png")


if __name__ == "__main__":
    main()
