"""Appendix 1-figure 1 (p. 72): precision-recall plot of T-bar prediction (initial, cascade, manual estimated).
Tier 3, digitized from the embedded raster; Appendix 1-figure 1-source data 1 not available locally.
Writes figures/afig1.csv and work/afig1_overlay.png. Shared code: tools/fc_pr.py."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_pr  # noqa: E402

rx, ry, rows = fc_pr.extract(72, ["initial", "cascade"], [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                             [0.98, 0.96, 0.94, 0.92, 0.90, 0.88, 0.86], {14, 89}, (325, 8, 548, 92),
                             HERE / "afig1.csv", HERE.parent / "work" / "afig1_overlay.png",
                             "Appendix 1-figure 1 of Scheffer et al. 2020 (eLife 9:e57443), p. 72: precision-recall plot of T-bar prediction.")
print(rx, ry, [r for r in rows if r[0] == "manual estimated"])
