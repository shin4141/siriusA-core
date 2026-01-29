import argparse
import json
import os
import sys

def _parse_args():
    # backward compatible:
    #   python chain_cli.py <pre> <tx> <out>
    #   python chain_cli.py --pre <pre> --tx <tx> --out <out>
    if len(sys.argv) >= 4 and not sys.argv[1].startswith("--"):
        return argparse.Namespace(pre_path=sys.argv[1], tx_path=sys.argv[2], out_path=sys.argv[3])

    p = argparse.ArgumentParser()
    p.add_argument("--pre", dest="pre_path", required=True)
    p.add_argument("--tx", dest="tx_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    return p.parse_args()

def main():
    args = _parse_args()

    with open(args.pre_path, "r", encoding="utf-8") as f:
        pre = json.load(f)
    with open(args.tx_path, "r", encoding="utf-8") as f:
        tx = json.load(f)

    # keep your existing merge logic here
    # severity=max, evidence=union
    from src.siriusa_core.chain import chain_merge  # ←もし無いなら既存ロジックをそのまま使う
    out = chain_merge(pre, tx)

    os.makedirs(os.path.dirname(args.out_path) or ".", exist_ok=True)
    with open(args.out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

