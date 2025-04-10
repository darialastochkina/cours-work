import os
import sys
import warnings
warnings.filterwarnings("ignore")

os.system(f"{sys.executable} -m pytest -p no:warnings")
