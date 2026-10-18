"""sfig5c: map the 3D laser SCM colour image to depth through its colour bar (tier 3). See sfig_scm.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfig_scm import write  # noqa: E402

write("sfig5c")
