# pyAAscan

AAscan은 변이 도입(예: 알라닌 스캐닝) 실험을 위한 프라이머(Primer)를 설계해주는 파이썬 프로그램입니다.
이 스크립트는 **파이썬 패키지로 임포트**해서 쓸 수도 있고, **명령줄(Command Line)에서 실행**할 수도 있습니다.

---

## 명령줄에서 사용하기

명령줄에서 실행하려면 아래 3가지 정보를 입력해야 합니다:

1. **DNA 서열 파일**
   프라이머를 설계할 DNA 서열이 들어있는 텍스트 파일입니다.
   (예: `-seq pBAD-LEH.gb`)

2. **시작 코돈의 인덱스**
   변이를 넣을 아미노산의 첫 번째 코돈이 DNA 서열에서 어디서 시작하는지 0부터 세는 인덱스입니다.
   (예: `-cod 30`)

3. **변이 정보**
   - 한 개의 변이만 설계할 때는 `-mut` 옵션에 `[원래 아미노산][번호][새 아미노산]` 형식으로 입력합니다.
     (예: `-mut S21R` → 21번 아미노산을 S에서 R로 바꿈)
   - 여러 개의 변이를 한 번에 설계할 때는 각 변이를 한 줄에 하나씩 적은 텍스트 파일을 만들어 `-mutf` 옵션으로 입력합니다.

### 실행 예시

- 단일 변이:
  ```bash
  python3 pyAAscan.py -seq pBAD-LEH.gb -cod 30 -mut S21R
  ```

- 여러 변이:
  ```bash
  python3 pyAAscan.py -seq pBAD-LEH.gb -cod 30 -mutf mutfile.txt
  ```

---

## 입력 파일 형식

- DNA 서열 파일은 ATGC 문자만 저장됩니다.
- 파일에서 숫자, 공백, ATGC만 읽어들이고, 그 외 문자는 무시합니다.
- FASTA, EMBL, GCG, GeneBank 등 다양한 형식의 파일을 사용할 수 있습니다.

---

## 추가 옵션

- **프라이머 길이**: 최소(-minl), 최대(-maxl)
- **Tm(녹는점)**: 최소(-mintm), 최대(-maxtm), 최대 차이(-maxdtm)
- **오버랩 길이**: 최소(-mino), 최대(-maxo)
- **GC clamp 품질**: 최소(-mincg)
- 더 많은 옵션은 `-h` 또는 `--help`로 확인할 수 있습니다.

---

## 알라닌 스캐닝 모드

- AAscan의 원래 목적은 알라닌 스캐닝 프라이머 설계입니다.
- `--aascan` 플래그를 사용하면, 변이 번호만 입력해도 설계가 가능합니다.

---

## 파이썬 패키지로 사용하기

AAscan을 파이썬 코드에서 직접 불러와서, 여러 변이에 대해 반복적으로 프라이머를 설계할 수 있습니다.

```python
import pyaascan as aa

mutations = ['S21R', 'Q7P']

for mut in mutations:
    # 원하는 아미노산의 대표 코돈 2개 선택
    codon1, codon2 = aa.BestCodons(mut[-1])

    # 프라이머 생성
    primers = aa.Mutate(seq_in=seq_in, cod1pos=30, mutpos=int(mut[1:-1]), codon1=codon1, codon2=codon2, outputmode='short')
    print(primers)

    # 각 프라이머의 Tm 출력
    for primer in primers:
        primer_noheader = primer.split(' ')[-1]
        print(aa.PrimerTm(primer_noheader))
```

---

## 기타 정보

- 별도의 추가 패키지 설치가 필요 없습니다.
- 오픈소스이며, 원본 코드는 [AAscan GitHub](https://github.com/dbv123w/AAScan)에서 확인할 수 있습니다.


# 추가 설명

아래는 CLI 프로그램을 실행하는 예시 커맨드입니다.

```bash
uv run python src/pyaascan/cli.py \
  --sequencefile tests/example_sequence.txt \
  --codonpos 120 \
  --mutpos 41 \
  --codon1 GCG \
  --codon2 GCA \
  --codon3 GGT \
  --codon4 GGC \
  --minlen 18 \
  --maxlen 35 \
  --minGCcl 2 \
  --mintm 60 \
  --maxtm 70 \
  --outputmode long1 \
  --verbose
```

이 커맨드는 지정한 조건에 맞는 변이 프라이머 후보를 터미널에 출력합니다.

- example_sequence.txt에는 5'→3' 방향의 DNA 서열이 텍스트로 들어 있습니다.
- --codonpos 120은 변이시킬 코돈의 0-based 시작 위치입니다.
- --mutpos 41은 변이 위치(1-based, 출력용)입니다.
- 기타 옵션은 필요에 따라 조정할 수 있습니다.

## Unittest

```bash
uv run python -m unittest tests/test_cli.py
```
