"""
[04] 실제 메모리 읽기 검증
────────────────────────────────────────────────────────────────
확인 항목
    - ctypes 로 ob_item 버퍼의 실제 메모리 값을 읽는다
    - 읽은 값이 id(list_b[i]) 와 일치하는지 확인
    - 버퍼가 PyObject* 포인터 배열임을 메모리 레벨에서 직접 증명
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


def read_ptr_at(base_addr: int, idx: int) -> int:
    """버퍼의 idx 번째 슬롯에 저장된 포인터 값을 읽는다."""
    slot_addr = base_addr + idx * ctypes.sizeof(ctypes.c_void_p)
    return ctypes.c_size_t.from_address(slot_addr).value


# ── 더미 클래스 ───────────────────────────────────────────────────
class Dummy:
    """속성, 메서드, 슬롯 아무것도 없는 빈 클래스."""
    pass


# ── 실행 ─────────────────────────────────────────────────────────
list_b  = []
objects = []

for _ in range(10):
    obj = Dummy()
    objects.append(obj)
    list_b.append(obj)

info     = list_internals(list_b)
buf_addr = info["ob_item"]

print(SEP)
print("[04] 실제 메모리 읽기 검증 — buf[i] == id(list_b[i])?")
print(SEP)

print()
print(f"  list_b 주소  : 0x{info['list_id']:016x}")
print(f"  버퍼(ob_item): 0x{buf_addr:016x}")
print(f"  원소 수      : {info['length']}")
print()

header = f"  {'#':>3}  {'id(list_b[i])':>18}  {'buf[i] (ctypes 읽기)':>18}  결과"
print(header)
print("  " + "-" * 58)

all_ok = True

for i in range(len(list_b)):
    expected = id(list_b[i])
    actual   = read_ptr_at(buf_addr, i)
    match    = "ok" if expected == actual else "FAIL"
    if expected != actual:
        all_ok = False
    print(
        f"  {i:>3}  "
        f"0x{expected:016x}  "
        f"0x{actual:016x}  {match}"
    )

print()
print(f"  전체 결과: {'전부 일치' if all_ok else '불일치 발생'}")
print()
print("  결론:")
print("    buf[i] 의 값 == id(list_b[i])")
print("    버퍼는 Python 오브젝트의 주소(포인터)를 8 B 간격으로 저장한")
print("    단순 포인터 배열임을 실제 메모리 접근으로 확인.")
print()

# 주소 산술 확인
print("  주소 산술 확인 (buf_addr + i * 8 이 각 슬롯 위치):")
for i in range(min(4, len(list_b))):
    slot = buf_addr + i * 8
    print(f"    buf + {i} * 8 = 0x{slot:016x}  -> 0x{read_ptr_at(buf_addr, i):016x}")
print()
