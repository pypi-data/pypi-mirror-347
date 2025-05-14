from typing import Dict, List

CODON_TABLE: Dict[str, str] = {
    # 표준 유전암호 표(Table 1, NCBI/GenScript 기준)
    # Phenylalanine
    "TTT": "F",
    "TTC": "F",
    # Leucine
    "TTA": "L",
    "TTG": "L",
    "CTT": "L",
    "CTC": "L",
    "CTA": "L",
    "CTG": "L",
    # Isoleucine
    "ATT": "I",
    "ATC": "I",
    "ATA": "I",
    # Methionine (Start)
    "ATG": "M",
    # Valine
    "GTT": "V",
    "GTC": "V",
    "GTA": "V",
    "GTG": "V",
    # Serine
    "TCT": "S",
    "TCC": "S",
    "TCA": "S",
    "TCG": "S",
    "AGT": "S",
    "AGC": "S",
    # Proline
    "CCT": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    # Threonine
    "ACT": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    # Alanine
    "GCT": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    # Tyrosine
    "TAT": "Y",
    "TAC": "Y",
    # Histidine
    "CAT": "H",
    "CAC": "H",
    # Glutamine
    "CAA": "Q",
    "CAG": "Q",
    # Asparagine
    "AAT": "N",
    "AAC": "N",
    # Lysine
    "AAA": "K",
    "AAG": "K",
    # Aspartic Acid
    "GAT": "D",
    "GAC": "D",
    # Glutamic Acid
    "GAA": "E",
    "GAG": "E",
    # Cysteine
    "TGT": "C",
    "TGC": "C",
    # Tryptophan
    "TGG": "W",
    # Arginine
    "CGT": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AGA": "R",
    "AGG": "R",
    # Glycine
    "GGT": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
    # Stop codons
    "TAA": "*",
    "TAG": "*",
    "TGA": "*",
}


def translate_codon(codon: str) -> str:
    """코돈을 아미노산으로 변환"""
    return CODON_TABLE.get(codon.upper(), "@")


def best_codons(res: str) -> List[str]:
    """E.coli에서 각 아미노산별 선호 코돈 2개 반환"""
    topcodons = {
        "R": ["CGT", "CGC"],
        "H": ["CAT", "CAC"],
        "K": ["AAA", "AAG"],  # ...
    }
    if res in topcodons:
        return topcodons[res]
    else:
        raise ValueError(f"Not a canonical amino acid: {res}")


def codon_match_score(c1: str, c2: str) -> int:
    """두 코돈의 유사도 점수 계산"""
    score = 0
    for i, j in zip(c1.upper(), c2.upper()):
        if i == j:
            score += 2 if i in {"G", "C"} else 1
    return score


def translate_oligo(
    sequence: str, startpos: int = 0, ignore_incomplete: bool = True
) -> str:
    """서열을 코돈 단위로 번역"""
    out = ""
    for i in range(startpos, len(sequence), 3):
        codon = sequence[i : i + 3]
        if len(codon) != 3 and ignore_incomplete:
            continue
        out += translate_codon(codon)
    return out
