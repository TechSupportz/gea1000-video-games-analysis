"""Shared look for the multiplayer story charts, so every slide matches."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import PercentFormatter

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#1f2328", "#6b7280", "#e7e7e3"
# matched to the slide deck: navy bg #1c4587, gold accent #ffd966
# multiplayer = deck navy, single-player = quiet slate, same on every chart (Japan too)
SP, MP = "#8c96a8", "#1c4587"
HOME, HANDHELD = "#2a9d8f", "#e09f3e"
# Japan callout = gold band like the deck accent, dark amber label so it still reads on white
SPOTLIGHT, SPOTLIGHT_BAND = "#9a6700", "#ffd966"
TIER_RAMP = ["#dbe3f1", "#a9bbdb", "#6f8cc0", "#1c4587", "#0f2a57"]
RR_CMAP = LinearSegmentedColormap.from_list("rr", ["#1c4587", "#f2f2f0", "#e09f3e"])


def use_style():
    # static DM Sans weights cut from the variable font (matplotlib can't pick weights from a variable font)
    for path in (Path(__file__).resolve().parent / "fonts").glob("DMSans-*.ttf"):
        font_manager.fontManager.addfont(str(path))
    plt.rcParams.update({
        "font.family": "DM Sans", "font.weight": "medium", "font.size": 11, "text.color": INK,
        "axes.titleweight": "bold", "axes.labelweight": "medium",
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "axes.linewidth": 1,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
        "grid.color": GRID, "grid.linewidth": 1,
        "xtick.color": INK, "ytick.color": MUTED, "xtick.major.size": 0, "ytick.major.size": 0,
        "xtick.labelsize": 11, "ytick.labelsize": 10,
        "legend.frameon": False, "legend.fontsize": 10,
    })


def titled(ax, title, subtitle=None):
    # left-aligned title with a quieter line underneath for the benchmark / sample
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=INK, pad=30 if subtitle else 14)
    if subtitle:
        ax.text(0, 1.035, subtitle, transform=ax.transAxes, fontsize=10.5, color=MUTED, va="bottom")


def bar_label(ax, x, value, detail, text="{:.1f}%"):
    ax.annotate(text.format(value), (x, value), xytext=(0, 17), textcoords="offset points",
                ha="center", fontsize=12.5, fontweight="semibold", color=INK)
    ax.annotate(detail, (x, value), xytext=(0, 4), textcoords="offset points",
                ha="center", fontsize=9, color=MUTED)


def paired_bars(ax, groups, colors, names, edges=None, top=100, legend="upper right"):
    """groups = [(tick label, [(pct, k, n) for value 0 and 1])]"""
    for x, (_, rows) in enumerate(groups):
        for value, (pct, k, n) in enumerate(rows):
            xo = x + (value - .5) * .36
            ax.bar(xo, pct, width=.33, color=colors[value], zorder=3,
                   edgecolor=edges[value] if edges else SURFACE, linewidth=1.8 if edges else 2,
                   label=names[value] if x == 0 else None)
            bar_label(ax, xo, pct, f"{k}/{n}")
    ax.set_xticks(range(len(groups)), [g[0] for g in groups])
    ax.set_xlim(-.6, len(groups) - .4)
    ax.set_ylim(0, top)
    ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.legend(loc=legend, ncol=2, handlelength=1.2, columnspacing=1.2)


def japan_spotlight(ax, x):
    # faint gold band + amber tick label so Japan stands out before the Japan slide (call after paired_bars)
    ax.axvspan(x - .48, x + .48, color=SPOTLIGHT_BAND, alpha=.22, lw=0, zorder=0)
    label = ax.get_xticklabels()[x]
    label.set_color(SPOTLIGHT)
    label.set_fontweight("bold")
