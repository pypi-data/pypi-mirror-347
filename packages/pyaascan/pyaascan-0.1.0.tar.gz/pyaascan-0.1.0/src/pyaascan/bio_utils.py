from typing import List


def primer_tm(primer: str) -> float:
    """GC 함량 기반 프라이머 Tm 계산"""
    gc_count = sum(1 for i in primer if i.upper() in {"G", "C"})
    skip_count = sum(1 for i in primer if i.upper() not in {"G", "C", "A", "T"})
    return round(64.9 + 41 * (gc_count - 16.4) / (len(primer) - skip_count), 1)


def gc_content(primer: str) -> float:
    """GC 함량 비율 반환"""
    gc_count = sum(1 for i in primer if i.upper() in {"G", "C"})
    return round(gc_count / len(primer), 2)


def complement_nucleotide(ch: str) -> str:
    """염기 상보 매칭"""
    complement = {
        "A": "T",
        "a": "t",
        "T": "A",
        "t": "a",
        "G": "C",
        "g": "c",
        "C": "G",
        "c": "g",
        "X": "Y",
        "x": "y",
        "Y": "X",
        "y": "x",
        "N": "N",
        "n": "n",
    }
    return complement.get(ch, ch)


def rc_oligo(primer: str) -> str:
    """역상보 서열 생성"""
    return "".join(complement_nucleotide(i) for i in reversed(primer))
