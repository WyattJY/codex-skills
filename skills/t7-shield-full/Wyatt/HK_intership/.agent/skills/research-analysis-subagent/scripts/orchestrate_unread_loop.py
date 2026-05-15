import argparse
from pathlib import Path
from select_next_unread import select_next_unread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default="downloads/MoE")
    parser.add_argument("--order", choices=["name", "mtime"], default="name")
    parser.add_argument("--require-paper-md", action="store_true")
    parser.add_argument("--max", type=int, default=0)
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser().resolve()
    if not base_dir.is_dir():
        raise SystemExit(f"Base dir not found: {base_dir}")

    count = 0
    while True:
        if args.max > 0 and count >= args.max:
            break
        nxt = select_next_unread(base_dir, args.order, args.require_paper_md)
        if nxt is None:
            break
        print(str(nxt))
        count += 1


if __name__ == "__main__":
    main()
