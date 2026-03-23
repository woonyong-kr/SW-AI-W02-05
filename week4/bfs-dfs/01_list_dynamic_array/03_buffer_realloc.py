"""
[03] 버퍼 재할당 추적 — 동적 배열 증명
────────────────────────────────────────────────────────────────
확인 항목
    - id(list_b)  : Dummy 를 계속 추가해도 리스트 오브젝트 주소 불변
    - ob_item     : 용량(capacity) 초과 시 새 주소로 재할당
    - id(obj)     : 개별 Dummy 오브젝트 주소 불변
    - CPython over-allocation 성장 패턴 확인
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


# ── 더미 클래스 ───────────────────────────────────────────────────
class Dummy:
    """속성, 메서드, 슬롯 아무것도 없는 빈 클래스."""
    pass


# ── 실행 ─────────────────────────────────────────────────────────
list_b  = []
objects = []   # GC 수거 방지 — 레퍼런스 유지 필수

prev_buf    = list_internals(list_b)["ob_item"]
prev_listid = id(list_b)

print(SEP)
print("[03] Dummy 20개 추가 — 내부 버퍼 재할당 추적")
print(SEP)

header = (
    f"  {'#':>3}  "
    f"{'id(obj)':>18}  "
    f"{'id(list_b)':>18}  "
    f"{'ob_item':>18}  "
    f"{'cap':>4}  비고"
)
print()
print(header)
print("  " + "-" * 86)

for i in range(20):
    obj = Dummy()
    objects.append(obj)
    list_b.append(obj)

    info = list_internals(list_b)
    note = ""

    if info["ob_item"] != prev_buf:
        note = "[realloc]"
        prev_buf = info["ob_item"]

    if info["list_id"] != prev_listid:
        note += " [list moved?!]"   # 정상 실행 시 출력되지 않아야 함

    print(
        f"  {i:>3}  "
        f"0x{id(obj):016x}  "
        f"0x{info['list_id']:016x}  "
        f"0x{info['ob_item']:016x}  "
        f"{info['allocated']:>4}  {note}"
    )

print()
print("  결론:")
print("    id(list_b)  -- 단 한 번도 변하지 않음 (리스트 오브젝트는 고정)")
print("    ob_item     -- capacity 초과 시 새 주소로 재할당 (동적 배열의 핵심)")
print("    id(obj)     -- 각 Dummy 오브젝트 주소 불변 (Python 오브젝트는 이동 없음)")
print()
print("  CPython capacity 성장 패턴: 0 -> 4 -> 8 -> 16 -> 25 -> ...")
print("  공식: new_cap = old_cap + (old_cap >> 3) + (3 if old_cap < 9 else 6)")
print()
