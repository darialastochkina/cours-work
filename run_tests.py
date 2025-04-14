import os
import sys
import warnings

from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
os.system(f"{sys.executable} -m pytest -p no:warnings")
