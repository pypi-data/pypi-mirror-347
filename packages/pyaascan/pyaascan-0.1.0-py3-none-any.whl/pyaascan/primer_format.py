from typing import Optional
from .bio_utils import primer_tm, gc_content


def primer_long_format1(
    mutpos: int, strand: str, gc_clamp: int, ann_len: int, primer: str, fullprimer: str
) -> str:
    """
    긴 형식 1: 프라이머 정보 상세 출력
    """
    return (
        f"{mutpos}_{strand} {primer} "
        f"len={len(primer)} "
        f"Tm={primer_tm(primer)} "
        f"Tmfull={primer_tm(fullprimer)} "
        f"GCclamp={gc_clamp} "
        f"AnnLenF={ann_len} "
        f"GCcontent={gc_content(fullprimer)} "
        f"{fullprimer}"
    )


def primer_long_format2(
    mutpos: int,
    strand: str,
    ann_len: int,
    primer: str,
    fullprimer: str,
    tm: Optional[float] = None,
    tm_full: Optional[float] = None,
    gc_content_val: Optional[float] = None,
) -> str:
    """
    긴 형식 2: 프라이머 정보 상세 출력 (옵션 파라미터 포함)
    """
    tm_val = tm if tm is not None else primer_tm(primer)
    tm_full_val = tm_full if tm_full is not None else primer_tm(fullprimer)
    gc_val = gc_content_val if gc_content_val is not None else gc_content(fullprimer)
    return (
        f"{mutpos}_{strand} {primer} "
        f"len={len(primer)} "
        f"Tm={tm_val} "
        f"Tmfull={tm_full_val} "
        f"AnnLenF={ann_len} "
        f"GCcontent={gc_val} "
        f"{fullprimer}"
    )


def primer_short_format(mutpos: int, strand: str, primer: str) -> str:
    """
    짧은 형식: 위치, 방향, 프라이머 서열만 출력
    """
    return f"{mutpos}_{strand} {primer}"


def primer_mfasta_format(mutpos: int, strand: str, primer: str) -> str:
    """
    mfasta 형식: FASTA 스타일로 출력
    """
    return f">{mutpos}_{strand}\n{primer}"
