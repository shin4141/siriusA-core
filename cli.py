import argparse
import json
import os
import sys

def _parse_args():
    # Backward compatible:
    #  A) python cli.py <in>
    #  B) python cli.py <in> <out>
    #  C) python cli.py --in <in> --out <out>
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        in_path = sys.argv[1]
        out_path = sys.argv[2] if len(sys.argv) >= 3 else None
        return argparse.Namespace(in_path=in_path, out_path=out_path)

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=False, default=None)
    return p.parse_args()

def main():
    args = _parse_args()

    with open(args.in_path, "r", encoding="utf-8") as f:
        req = json.load(f)

    from src.siriusa_core.gate import gate
    result = gate(req)

    # If --out omitted (or only one arg), print to stdout (CI-friendly)
    if not args.out_path:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    os.makedirs(os.path.dirname(args.out_path) or ".", exist_ok=True)
    with open(args.out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()


