import sys
from pathlib import Path

src_dir = Path(__file__).resolve().parent.parent
project_root = src_dir.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))