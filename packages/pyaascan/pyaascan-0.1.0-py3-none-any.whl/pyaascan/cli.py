import argparse
from .primer_design import mutate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Site-directed mutagenesis primer design CLI"
    )
    parser.add_argument(
        "-s",
        "--sequencefile",
        type=str,
        required=True,
        help="Input DNA sequence file (plain text, 5'→3')",
    )
    parser.add_argument(
        "-c",
        "--codonpos",
        type=int,
        required=True,
        help="0-based start position of the codon to mutate",
    )
    parser.add_argument(
        "-m",
        "--mutpos",
        type=int,
        required=True,
        help="1-based mutation position (for output labeling)",
    )
    parser.add_argument("--codon1", type=str, default="GCG", help="Alternative codon 1")
    parser.add_argument("--codon2", type=str, default="GCA", help="Alternative codon 2")
    parser.add_argument("--codon3", type=str, default="GGT", help="Alternative codon 3")
    parser.add_argument("--codon4", type=str, default="GGC", help="Alternative codon 4")
    parser.add_argument("--minlen", type=int, default=18, help="Minimum primer length")
    parser.add_argument("--maxlen", type=int, default=60, help="Maximum primer length")
    parser.add_argument(
        "--minGCcl", type=int, default=2, help="Minimum GC clamp (3' end, last 5 nt)"
    )
    parser.add_argument("--mintm", type=float, default=60.0, help="Minimum Tm")
    parser.add_argument("--maxtm", type=float, default=70.0, help="Maximum Tm")
    parser.add_argument(
        "-o",
        "--outputmode",
        type=str,
        choices=["long1", "short", "mfasta"],
        default="long1",
        help="Output format",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def read_sequence(filename: str) -> str:
    with open(filename, "r") as f:
        seq = f.read()
    # Remove whitespace and line breaks
    return "".join(seq.split())


def main() -> None:
    args = parse_args()
    seq = read_sequence(args.sequencefile)
    primers = mutate(
        seq_in=seq,
        cod1pos=args.codonpos,
        mutpos=args.mutpos,
        codon1=args.codon1,
        codon2=args.codon2,
        codon3=args.codon3,
        codon4=args.codon4,
        minlen=args.minlen,
        maxlen=args.maxlen,
        minGCcl=args.minGCcl,
        mintm=args.mintm,
        maxtm=args.maxtm,
        outputmode=args.outputmode,
        verbose=args.verbose,
    )
    for line in primers:
        print(line)


if __name__ == "__main__":
    main()
