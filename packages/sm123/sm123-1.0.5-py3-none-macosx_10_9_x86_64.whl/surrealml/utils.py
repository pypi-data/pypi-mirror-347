from pathlib import Path
import json, sys

def read_dynamic_lib_version() -> str:
    try:
        pkg_root = Path(__file__).resolve().parent.parent
        cfg_path = pkg_root / 'config.json'

        with cfg_path.open('r') as f:
            cfg = json.load(f)
            return cfg['dynamic_lib_version']
    except Exception as e:
        print(f"Error loading version from '{cfg_path}': {e}", file=sys.stderr)
        sys.exit(1)