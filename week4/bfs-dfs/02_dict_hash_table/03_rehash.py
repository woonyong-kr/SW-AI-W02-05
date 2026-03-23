"""
[03] 재해시(rehash) — 해시 값 불변 & 슬롯 위치 재배치
────────────────────────────────────────────────────────────────
확인 항목
    - hash(key) 는 딕셔너리 크기와 무관하게 항상 동일한 값
    - 버킷 수가 바뀌면 slot = hash(key) & (size - 1) 이 달라진다
    - resize 전후 슬롯 번호 비교 — 같은 키라도 위치가 바뀜
    - 해시 값 자체는 키 오브젝트에 귀속되므로 절대 변하지 않음
"""

import ctypes

SEP = "-" * 60


def get_bucket_count(d: dict) -> int:
    """PyDictKeysObject.dk_size 를 ctypes 로 직접 읽는다 (Python 3.10)."""
    ma_keys_addr = ctypes.c_size_t.from_address(id(d) + 32).value
    return ctypes.c_ssize_t.from_address(ma_keys_addr + 8).value


def slot_of(key, bucket_count: int) -> int:
    """버킷 수 bucket_count 에서 key 의 초기 슬롯 번호를 반환한다."""
    return hash(key) & (bucket_count - 1)


# ── 실행 ─────────────────────────────────────────────────────────
print(SEP)
print("[03] 재해시 — 해시 값 불변 & 슬롯 위치 재배치")
print(SEP)

# --- 1) 해시 값 불변 증명 -----------------------------------------------
print()
print("  [1] hash(key) 는 딕셔너리 크기와 무관하다")
print()

sample_keys = ["apple", "banana", "cherry", "date", "elderberry"]
hash_before = {k: hash(k) for k in sample_keys}

d = {}
for k in sample_keys:
    d[k] = k

# 충분히 더 추가해 resize 를 반드시 유발
for i in range(50):
    d[f"extra_{i}"] = i

hash_after = {k: hash(k) for k in sample_keys}

header = f"  {'key':>12}  {'hash (before)':>20}  {'hash (after)':>20}  결과"
print(header)
print("  " + "-" * 64)
for k in sample_keys:
    b = hash_before[k]
    a = hash_after[k]
    result = "ok (같음)" if b == a else "FAIL (달라짐)"
    print(f"  {k:>12}  {b:>20}  {a:>20}  {result}")

print()
print("  결론: hash(key) 는 키 오브젝트 자체에 귀속된다.")
print("        딕셔너리 크기(버킷 수)가 바뀌어도 해시 값은 변하지 않는다.")

# --- 2) 슬롯 번호 재배치 증명 ----------------------------------------------
print()
print()
print("  [2] resize 전후 슬롯 번호 비교")
print()

d2 = {}
snapshot_before = None
size_before = None

# 항목을 추가하며 resize 직전 슬롯 스냅샷 찍기
keys_to_track = [f"key_{i}" for i in range(6)]
for k in keys_to_track:
    d2[k] = k

size_before = get_bucket_count(d2)
slots_before = {k: slot_of(k, size_before) for k in keys_to_track}

# resize 유발 (충분히 더 추가)
extra = 0
size_after = size_before
while size_after == size_before:
    d2[f"pad_{extra}"] = extra
    extra += 1
    size_after = get_bucket_count(d2)

slots_after = {k: slot_of(k, size_after) for k in keys_to_track}

print(f"  resize 전 버킷 수 : {size_before}")
print(f"  resize 후 버킷 수 : {size_after}")
print()

header2 = f"  {'key':>8}  {'slot (before)':>14}  {'slot (after)':>13}  변화"
print(header2)
print("  " + "-" * 52)
for k in keys_to_track:
    sb = slots_before[k]
    sa = slots_after[k]
    changed = "위치 변경" if sb != sa else "동일"
    print(f"  {k:>8}  {sb:>14}  {sa:>13}  {changed}")

print()
print("  결론:")
print("    hash(key) 는 그대로지만, 버킷 수(mask)가 바뀌면")
print("    slot = hash(key) & (new_size - 1) 이 달라진다.")
print("    CPython 은 resize 시 모든 기존 항목을 새 버킷에 재삽입(rehash)한다.")
print()
