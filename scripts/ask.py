"""Usage: python -m scripts.ask "refund kitne din mein?" [-k 5]"""
import argparse

from pramaan.answer import answer, label


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()

    result = answer(args.question, k=args.k)
    print("\nANSWER\n" + result["answer"])
    print("\nRETRIEVED")
    for c in result["chunks"]:
        print(f"  {c['score']:.3f}  {label(c)}  {c['content'][:80]!r}")


if __name__ == "__main__":
    main()
