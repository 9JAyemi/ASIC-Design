#!/usr/bin/env python3
"""Plot energy per cycle vs clock frequency for each cell group.

Reads reports/<group>/energy.csv (written by lab2.sh), with columns
clk_ns, PDyn_mW, PLeak_mW, EDyn_pJ, ELeak_pJ, Etotal_pJ.
Frequency (MHz) = 1000 / clk_period (ns).

Each synthesized design point is drawn as a marker, and straight lines
connect adjacent points.

Output (in plots/):
  energy_<group>.png   dynamic, leakage and total energy vs frequency for one group
  energy_compare.png   one panel per energy type, all groups overlaid

Usage:  python3.12 plot_energy.py [--log] [GROUP ...]
        (default groups: SVT20 LVT20 LVT16; --log uses log-scale axes)
"""
import argparse
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")  # no display needed on the server
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = ["SVT20", "LVT20", "LVT16"]
ENERGIES = [("EDyn_pJ", "Dynamic energy (pJ)", "#4285F4"),
            ("ELeak_pJ", "Leakage energy (pJ)", "#DB4437"),
            ("Etotal_pJ", "Total energy (pJ)", "#F4B400")]
GROUP_COLORS = {"SVT20": "#4285F4", "LVT20": "#DB4437", "LVT16": "#0F9D58"}


def load(group):
    """Return rows for a group, sorted by frequency (low to high)."""
    path = os.path.join(HERE, "reports", group, "energy.csv")
    if not os.path.exists(path):
        # fallback: copy saved in results/
        path = os.path.join(HERE, "results", f"{group}_energy.csv")
    if not os.path.exists(path):
        print(f"skipping {group}: no energy.csv in reports/{group}/ or results/")
        return None
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            row = {k: float(v) for k, v in r.items()}
            row["f_MHz"] = 1000.0 / row["clk_ns"]
            rows.append(row)
    rows.sort(key=lambda r: r["f_MHz"])
    print(f"{group}: {len(rows)} points from {os.path.relpath(path, HERE)}")
    return rows


def style_axes(ax, title, log):
    if log:
        ax.set_xscale("log")
        ax.set_yscale("log")
    else:
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    ax.set_xlabel("Frequency (MHz)", fontweight="bold")
    ax.set_ylabel("Energy (pJ/cycle)", fontweight="bold")
    ax.set_title(title, loc="left", fontsize=13, color="#5f6368", fontweight="bold")
    ax.grid(True, which="major", color="#dddddd")
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def plot_group(group, rows, out_dir, log):
    f = [r["f_MHz"] for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    # total is drawn wider and underneath, so dynamic stays visible where leakage is ~0
    widths = {"EDyn_pJ": (1.6, 4.5, 3), "ELeak_pJ": (1.6, 4.5, 3), "Etotal_pJ": (4.0, 8, 2)}
    for col, label, color in ENERGIES:
        lw, ms, z = widths[col]
        ax.plot(f, [r[col] for r in rows], "-o", color=color, lw=lw, ms=ms, zorder=z, label=label)
    style_axes(ax, f"{group}: Energy (pJ/cycle) vs Frequency (MHz)", log)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
    fig.tight_layout()
    path = os.path.join(out_dir, f"energy_{group}{'_log' if log else ''}.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {os.path.relpath(path, HERE)}")


def plot_compare(data, out_dir, log):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    for ax, (col, label, _) in zip(axes, ENERGIES):
        for group, rows in data.items():
            ax.plot([r["f_MHz"] for r in rows], [r[col] for r in rows], "-o",
                    color=GROUP_COLORS.get(group), lw=1.8, ms=5, label=group)
        style_axes(ax, f"{label.replace(' (pJ)', '')} vs Frequency", log)
        ax.legend(frameon=False)
    fig.tight_layout()
    path = os.path.join(out_dir, f"energy_compare{'_log' if log else ''}.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"wrote {os.path.relpath(path, HERE)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("groups", nargs="*", default=GROUPS)
    ap.add_argument("--log", action="store_true", help="log-scale axes (default: linear)")
    args = ap.parse_args()

    out_dir = os.path.join(HERE, "plots")
    os.makedirs(out_dir, exist_ok=True)

    data = {}
    for g in args.groups:
        rows = load(g)
        if rows:
            data[g] = rows
            plot_group(g, rows, out_dir, args.log)
    if not data:
        sys.exit("no data found")
    if len(data) > 1:
        plot_compare(data, out_dir, args.log)


if __name__ == "__main__":
    main()
