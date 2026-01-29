import argparse
import json
import os
import sys

def _parse_args():
    if len(sys.argv) >= 3 and not sys.argv[1].startswith("--"):
        return argparse.Namespace(in_path=sys.argv[1], out_path=sys.argv[2])

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    return p.parse_args()

def main():
    args = _parse_args()

    with open(args.in_path, "r", encoding="utf-8") as f:
        req = json.load(f)

    from src.siriusa_core.gate import gate
    result = gate(req)

    os.makedirs(os.path.dirname(args.out_path) or ".", exist_ok=True)
    with open(args.out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

