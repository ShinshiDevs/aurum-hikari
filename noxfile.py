import os
import runpy
import sys

CI_PATH = "pipelines"

sys.path.append(os.getcwd())


for f in os.listdir(CI_PATH):
    if f.endswith(".nox.py"):
        runpy.run_path(os.path.join(CI_PATH, f))
