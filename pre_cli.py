import json
import sys
from pathlib import Path

# add ./src to import path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from siriusa_core.pre_guard import run_pre_guard, pre_artifact_to_dict


def main():
    if len(sys.argv) < 2:
        print("Usage: python pre_cli.py <path/to/pre_guard_request.json>")
        sys.exit(2)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        req = json.load(f)

    art = run_pre_guard(req)
    print(json.dumps(pre_artifact_to_dict(art), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
