import json
from pathlib import Path

import fractal_lif_converters

PACKAGE = "fractal_lif_converters"
PACKAGE_DIR = Path(fractal_lif_converters.__file__).parent
MANIFEST_FILE = PACKAGE_DIR / "__FRACTAL_MANIFEST__.json"
with MANIFEST_FILE.open("r") as f:
    MANIFEST = json.load(f)
    TASK_LIST = MANIFEST["task_list"]
