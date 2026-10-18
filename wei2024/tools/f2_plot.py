"""Shared re-plot helpers for the wei2024 Fig. 6/9/10 plotting scripts (fork F2)."""
import csv


def read_rows(path):
    """Rows of a CSV with '#' comment lines first, as dicts."""
    with open(path, newline="") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines))


RATE_COLOURS = {"0.10 Å/ps": "black", "0.1 Å/ps": "black", "0.25 Å/ps": "red", "0.50 Å/ps": "magenta",
                "0.75 Å/ps": "blue", "1.00 Å/ps": "olive", "1.50 Å/ps": "maroon", "2.00 Å/ps": "darkorange"}
