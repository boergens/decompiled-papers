"""Appendix 1-figure 2 (p. 73): precision-recall plot of end-to-end synapse prediction (initial, cascade, hybrid,
synful+, manual estimated). Tier 3, digitized from the embedded raster; Appendix 1-figure 2-source data 1 not available
locally. Writes figures/afig2.csv and work/afig2_overlay.png. Shared code: tools/fc_pr.py."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_pr  # noqa: E402

rx, ry, rows = fc_pr.extract(73, ["initial", "cascade", "hybrid", "synful+"], [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                             [0.9, 0.8, 0.7, 0.6, 0.5], {14, 136}, (325, 8, 548, 140),
                             HERE / "afig2.csv", HERE.parent / "work" / "afig2_overlay.png",
                             "Appendix 1-figure 2 of Scheffer et al. 2020 (eLife 9:e57443), p. 73: precision-recall plot of end-to-end synapse prediction.")
print(rx, ry, [r for r in rows if r[0] == "manual estimated"])
