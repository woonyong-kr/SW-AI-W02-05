"""
[04] 오픈 주소법 — CPython 탐사 알고리즘 시뮬레이션
────────────────────────────────────────────────────────────────
확인 항목
    - CPython 딕셔너리는 체이닝(chaining) 이 아닌 오픈 주소법 사용
    - 탐사 공식: perturb >>= 5; i = (5*i + 1 + perturb) & mask
    - 같은 초기 슬롯에 충돌하는 두 키를 찾고 탐사 경로 비교
    - 체이닝 방식과의 차이점 개념 설명
"""

SEP = "-" * 60

# CPython PERTURB_SHIFT = 5
PERTURB_SHIFT = 5


def probe_sequence(key, bucket_count: int, max_steps: int = 12) -> list:
    """
    CPython 오픈 주소법 탐사 순서를 시뮬레이션한다.
    반환값: 방문한 슬롯 번호 리스트
    """
    mask    = bucket_count - 1
    h       = hash(key)
    i       = h & mask
    perturb = h if h >= 0 else -h   # C unsigned 처럼 양수로 취급

    visited = [i]
    for _ in range(max_steps - 1):
        perturb >>= PERTURB_SHIFT
        i = (5 * i + 1 + perturb) & mask
        if i in visited:
            break
        visited.append(i)
    return visited


def find_collision_pair(bucket_count: int):
    """
    같은 초기 슬롯에 매핑되는 두 문자열 키를 찾아 반환한다.
    """
    mask = bucket_count - 1
    slot_map: dict = {}
    for i in range(10000):
        key  = f"key_{i}"
        slot = hash(key) & mask
        if slot in slot_map:
            return slot_map[slot], key, slot
        slot_map[slot] = key
    return None, None, None


# ── 실행 ─────────────────────────────────────────────────────────
print(SEP)
print("[04] 오픈 주소법 — CPython 탐사 알고리즘 시뮬레이션")
print(SEP)

# --- 1) 체이닝 vs 오픈 주소법 개념 비교 -----------------------------------
print()
print("  [1] 충돌 해결 방식 비교")
print()
print("  체이닝 (Chaining):")
print("    - 각 버킷에 링크드 리스트를 연결")
print("    - 충돌 시 리스트 끝에 노드를 추가")
print("    - 버킷 외부 메모리 사용 -> 캐시 미스 가능성 높음")
print("    - Java HashMap, Python 2 dict (부분적) 등에서 사용")
print()
print("  오픈 주소법 (Open Addressing):")
print("    - 모든 항목이 버킷 배열 안에 저장")
print("    - 충돌 시 탐사(probe) 함수로 다음 빈 슬롯을 찾음")
print("    - 캐시 친화적 (메모리 연속 접근)")
print("    - CPython dict 가 사용하는 방식")
print()

# --- 2) CPython 탐사 공식 설명 -------------------------------------------
print()
print("  [2] CPython 탐사 공식 (PERTURB_SHIFT = 5)")
print()
print("    초기: i = hash(key) & mask")
print("    반복: perturb >>= 5")
print("          i = (5 * i + 1 + perturb) & mask")
print()
print("  - perturb 는 hash 값의 상위 비트를 점진적으로 혼합")
print("  - 단순 선형 탐사보다 클러스터링을 효과적으로 줄임")
print("  - mask = bucket_count - 1 (항상 2의 거듭제곱)")
print()

# --- 3) 탐사 경로 시각화 ---------------------------------------------------
bucket_count = 8
print()
print(f"  [3] 탐사 경로 시각화 (버킷 수 = {bucket_count})")
print()

sample_keys = ["alpha", "beta", "gamma", "delta"]
for key in sample_keys:
    seq   = probe_sequence(key, bucket_count)
    h_val = hash(key)
    print(f"  key='{key}'  hash={h_val}  초기슬롯={h_val & (bucket_count-1)}")
    print(f"    탐사 순서: {' -> '.join(str(s) for s in seq)}")
    print()

# --- 4) 충돌 쌍 찾기 & 탐사 경로 비교 ------------------------------------
bucket_count2 = 16
key_a, key_b, collision_slot = find_collision_pair(bucket_count2)

print()
print(f"  [4] 충돌 시뮬레이션 (버킷 수 = {bucket_count2})")
print()

if key_a and key_b:
    print(f"  충돌 발견: '{key_a}' 와 '{key_b}' 모두 초기 슬롯 {collision_slot} 에 매핑")
    print()

    seq_a = probe_sequence(key_a, bucket_count2)
    seq_b = probe_sequence(key_b, bucket_count2)

    print(f"  '{key_a}' 탐사 경로: {' -> '.join(str(s) for s in seq_a)}")
    print(f"  '{key_b}' 탐사 경로: {' -> '.join(str(s) for s in seq_b)}")
    print()

    # 충돌 상황 도식
    print("  버킷 배열 (오픈 주소법 삽입 시뮬레이션):")
    buckets: list = [None] * bucket_count2

    def insert_key(key, bkts):
        mask = len(bkts) - 1
        h    = hash(key)
        i    = h & mask
        perturb = h if h >= 0 else -h
        step = 0
        while bkts[i] is not None:
            perturb >>= PERTURB_SHIFT
            i = (5 * i + 1 + perturb) & mask
            step += 1
        bkts[i] = key
        return i, step

    slot_a, steps_a = insert_key(key_a, buckets)
    slot_b, steps_b = insert_key(key_b, buckets)

    print(f"    '{key_a}' -> 슬롯 {slot_a} (탐사 {steps_a}회)")
    print(f"    '{key_b}' -> 슬롯 {slot_b} (탐사 {steps_b}회 / 충돌 후 이동)")
    print()
    print("    슬롯 내용:")
    for idx, val in enumerate(buckets):
        if val is not None:
            print(f"      [{idx:>2}] {val}")
        else:
            print(f"      [{idx:>2}] (empty)")
else:
    print("  충돌 쌍을 찾지 못했습니다.")

print()
print("  결론:")
print("    CPython dict 는 오픈 주소법을 사용한다.")
print("    충돌 시 perturb 기반 탐사로 다음 빈 슬롯을 찾는다.")
print("    체이닝과 달리 모든 값이 버킷 배열 안에 저장되며,")
print("    메모리가 연속적이어서 캐시 효율이 높다.")
print()
