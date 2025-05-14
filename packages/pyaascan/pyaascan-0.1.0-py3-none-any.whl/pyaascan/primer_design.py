from typing import List, Optional
from .bio_utils import primer_tm, gc_content, rc_oligo
from .codon_utils import best_codons, codon_match_score, translate_codon
from .primer_format import (
    primer_long_format1,
    primer_short_format,
    primer_mfasta_format,
)


def mutate(
    seq_in: str,
    cod1pos: int,
    mutpos: int,
    codon1: str = "GCG",
    codon2: str = "GCA",
    codon3: str = "GGT",
    codon4: str = "GGC",
    altset: Optional[List[str]] = None,
    minlen: int = 18,
    maxlen: int = 60,
    minGCcl: int = 2,
    mintm: float = 60.0,
    maxtm: float = 70.0,
    outputmode: str = "long1",
    verbose: bool = False,
) -> List[str]:
    """
    변이 도입 프라이머 후보를 설계하는 함수.
    seq_in: 입력 DNA 서열 (5'->3')
    cod1pos: 변이 코돈의 시작 위치 (0-based)
    mutpos: 변이 위치 (1-based, 인간 친화적)
    codon1~4: 변이 코돈 후보
    altset: 대체 코돈 리스트
    minlen, maxlen: 프라이머 길이 조건
    minGCcl: 3' GC clamp 최소 개수
    mintm, maxtm: Tm 조건
    outputmode: 출력 포맷 선택
    verbose: 상세 로그 출력
    """
    if altset is None:
        altset = [codon1, codon2, codon3, codon4]

    lines_out: List[str] = []
    seq_len = len(seq_in)
    mut_codon_start = cod1pos
    mut_codon_end = cod1pos + 3

    # 변이 코돈을 대체한 서열 생성
    for alt_codon in altset:
        seq_mut = seq_in[:mut_codon_start] + alt_codon + seq_in[mut_codon_end:]

        # 프라이머 길이 범위 내에서 후보 생성
        for flank_len in range(minlen, maxlen + 1):
            # forward primer
            start = max(0, mut_codon_start - flank_len // 2)
            end = min(seq_len, mut_codon_end + flank_len // 2)
            primer = seq_mut[start:end]
            fullprimer = primer  # 필요시 추가 가공

            # GC clamp 계산 (3' 말단 5개 중 G/C 개수)
            gc_clamp = sum(1 for i in primer[-5:] if i.upper() in {"G", "C"})

            # Tm 계산
            tm = primer_tm(primer)
            if (
                mintm <= tm <= maxtm
                and gc_clamp >= minGCcl
                and minlen <= len(primer) <= maxlen
            ):
                if outputmode == "long1":
                    line = primer_long_format1(
                        mutpos, "F", gc_clamp, len(primer), primer, fullprimer
                    )
                elif outputmode == "short":
                    line = primer_short_format(mutpos, "F", primer)
                elif outputmode == "mfasta":
                    line = primer_mfasta_format(mutpos, "F", primer)
                else:
                    line = primer
                lines_out.append(line)

            # reverse primer (역상보)
            rc_primer = rc_oligo(primer)
            rc_gc_clamp = sum(1 for i in rc_primer[-5:] if i.upper() in {"G", "C"})
            rc_tm = primer_tm(rc_primer)
            if (
                mintm <= rc_tm <= maxtm
                and rc_gc_clamp >= minGCcl
                and minlen <= len(rc_primer) <= maxlen
            ):
                if outputmode == "long1":
                    line = primer_long_format1(
                        mutpos, "R", rc_gc_clamp, len(rc_primer), rc_primer, rc_primer
                    )
                elif outputmode == "short":
                    line = primer_short_format(mutpos, "R", rc_primer)
                elif outputmode == "mfasta":
                    line = primer_mfasta_format(mutpos, "R", rc_primer)
                else:
                    line = rc_primer
                lines_out.append(line)

    if verbose:
        print(f"Generated {len(lines_out)} primers for mutation at position {mutpos}")

    return lines_out
