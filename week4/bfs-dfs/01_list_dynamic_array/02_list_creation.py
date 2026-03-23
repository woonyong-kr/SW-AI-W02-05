"""
[02] 두 리스트 생성 — 초기 상태 확인
────────────────────────────────────────────────────────────────
확인 항목
    - 빈 리스트의 ob_item 이 NULL(0x0) 임을 확인
      (아직 버퍼 메모리가 할당되지 않은 상태)
    - 두 리스트 오브젝트의 주소가 서로 다름
"""

import ctypes

SEP = "-" * 60


# ── CPython 내부 구조체 ────────────────────────────────────────────
class _PyListStruct(ctypes.Structure):
    _fields_ = [
        ("ob_refcnt",  ctypes.c_ssize_t),
        ("ob_type",    ctypes.c_void_p),
        ("ob_size",    ctypes.c_ssize_t),
        ("ob_item",    ctypes.c_void_p),   # 버퍼 주소 (핵심)
        ("allocated",  ctypes.c_ssize_t),
    ]


def list_internals(lst: list) -> dict:
    """리스트 내부 C 구조체를 읽어 주요 필드를 반환한다."""
    raw = _PyListStruct.from_address(id(lst))
    return {
        "list_id":   id(lst),
        "ob_item":   raw.ob_item or 0,
        "allocated": raw.allocated,
        "length":    raw.ob_size,
    }


# ── 실행 ─────────────────────────────────────────────────────────
list_a = []   # 비교용 (이후 아무것도 추가하지 않음)
list_b = []   # Dummy 오브젝트를 추가할 리스트

snap_a = list_internals(list_a)
snap_b = list_internals(list_b)

print(SEP)
print("[02] 두 리스트 생성 — 초기 상태")
print(SEP)

print()
print(f"  list_a")
print(f"    id(list_a)  = 0x{snap_a['list_id']:016x}")
print(f"    ob_item     = 0x{snap_a['ob_item']:016x}  (NULL)")
print(f"    len         = {snap_a['length']}")
print(f"    allocated   = {snap_a['allocated']}")

print()
print(f"  list_b")
print(f"    id(list_b)  = 0x{snap_b['list_id']:016x}")
print(f"    ob_item     = 0x{snap_b['ob_item']:016x}  (NULL)")
print(f"    len         = {snap_b['length']}")
print(f"    allocated   = {snap_b['allocated']}")

print()
print("  결론:")
print("    빈 리스트의 ob_item = 0x0")
print("    원소를 추가하기 전까지는 버퍼 메모리를 할당하지 않는다.")
print()
