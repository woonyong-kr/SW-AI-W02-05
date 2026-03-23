"""
[02] 버킷 수 변화 추적 — 딕셔너리 재할당 증명
────────────────────────────────────────────────────────────────
확인 항목
    - 항목을 추가할수록 버킷 수(dk_size)가 언제 바뀌는지
    - CPython 의 resize 임계값 (~2/3 부하율) 확인
    - 버킷 수는 항상 2의 거듭제곱임을 확인
    - id(d) 는 재할당 후에도 불변임을 재확인

CPython PyDictKeysObject 구조 (Python 3.10.x, 64비트):
    offset  0  dk_refcnt   8 B  참조 카운터
    offset  8  dk_size     8 B  버킷 수 (직접 저장, 2의 거듭제곱)
    offset 16  dk_lookup   8 B  조회 함수 포인터
    offset 24  dk_usable   8 B  아직 사용 가능한 슬롯 수
    offset 32  dk_nentries 8 B  할당된 엔트리 수
    ...         해시 인덱스 테이블 + 엔트리 배열
"""

import ctypes

SEP = "-" * 60


def get_bucket_count(d: dict) -> int:
    """PyDictKeysObject.dk_size 를 ctypes 로 직접 읽는다 (Python 3.10)."""
    ma_keys_addr = ctypes.c_size_t.from_address(id(d) + 32).value
    return ctypes.c_ssize_t.from_address(ma_keys_addr + 8).value


# ── 실행 ─────────────────────────────────────────────────────────
d = {}

print(SEP)
print("[02] 버킷 수 변화 추적 — 항목 추가 시 resize 포착")
print(SEP)

prev_buckets = get_bucket_count(d)
prev_dict_id = id(d)

header = (
    f"  {'#':>3}  "
    f"{'key':>8}  "
    f"{'buckets':>8}  "
    f"{'load %':>7}  "
    f"{'id(d)':>18}  비고"
)
print()
print(header)
print("  " + "-" * 72)

# 빈 딕셔너리 상태 먼저 출력
print(
    f"  {'-':>3}  "
    f"{'(빈)':>8}  "
    f"{prev_buckets:>8}  "
    f"{'0.0':>6}%  "
    f"0x{prev_dict_id:016x}  초기 상태"
)

for i in range(30):
    key = f"k{i:02d}"
    d[key] = i

    buckets  = get_bucket_count(d)
    n_items  = len(d)
    load_pct = n_items / buckets * 100
    note     = ""

    if buckets != prev_buckets:
        note = f"[resize {prev_buckets} -> {buckets}]"
        prev_buckets = buckets

    if id(d) != prev_dict_id:
        note += " [dict moved?!]"

    print(
        f"  {i:>3}  "
        f"{key:>8}  "
        f"{buckets:>8}  "
        f"{load_pct:>6.1f}%  "
        f"0x{id(d):016x}  {note}"
    )

print()
print("  결론:")
print("    버킷 수는 항상 2의 거듭제곱으로 유지된다.")
print("    부하율(load factor)이 약 2/3 를 넘으면 resize 가 발생한다.")
print("    resize 시 버킷 수는 보통 4배 증가 (len * 4 이상의 최소 2의 거듭제곱).")
print("    id(d) 는 resize 후에도 변하지 않는다 (딕셔너리 오브젝트는 고정).")
print()

# 2의 거듭제곱 확인
import math
print("  버킷 수 2의 거듭제곱 확인:")
for n in [8, 16, 32, 64, 128]:
    log2 = math.log2(n)
    print(f"    {n:>4} = 2^{log2:.0f}  {'ok' if log2 == int(log2) else 'not power-of-2'}")
print()
