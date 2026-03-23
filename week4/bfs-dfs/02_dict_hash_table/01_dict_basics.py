"""
[01] 딕셔너리 기본 메모리 구조
────────────────────────────────────────────────────────────────
확인 항목
    - sys.getsizeof() 로 dict 오브젝트 자체 크기 확인
    - id(d) : 항목을 추가해도 딕셔너리 오브젝트 주소 불변
    - CPython PyDictObject C 구조체 필드 개요
    - ma_keys 포인터 (PyDictKeysObject*) 주소 읽기
"""

import sys
import ctypes

SEP = "-" * 60


# ── CPython PyDictObject 오프셋 (64비트 Python 3.10) ────────────────
#   offset  0  ob_refcnt  8 B  참조 카운터
#   offset  8  ob_type    8 B  타입 포인터
#   offset 16  ma_used    8 B  실제 저장된 항목 수
#   offset 24  ma_version 8 B  버전 태그 (수정될 때마다 증가)
#   offset 32  ma_keys    8 B  PyDictKeysObject* 포인터 (버킷 배열)
#   offset 40  ma_values  8 B  값 배열 포인터 (split-table 모드; 보통 NULL)

def get_ma_keys_addr(d: dict) -> int:
    """PyDictObject.ma_keys 포인터 값을 읽는다."""
    return ctypes.c_size_t.from_address(id(d) + 32).value


# ── 실행 ─────────────────────────────────────────────────────────
d = {}

print(SEP)
print("[01] 딕셔너리 기본 메모리 구조")
print(SEP)

print()
print("  CPython PyDictObject 구조 (64비트 기준):")
print("    offset  0  ob_refcnt   8 B  참조 카운터")
print("    offset  8  ob_type     8 B  타입 포인터")
print("    offset 16  ma_used     8 B  실제 저장 항목 수")
print("    offset 24  ma_version  8 B  수정 버전 태그")
print("    offset 32  ma_keys     8 B  PyDictKeysObject* (버킷 배열 포인터)")
print("    offset 40  ma_values   8 B  값 배열 포인터 (split-table 시 사용)")
print()

print(f"  빈 dict 크기         : {sys.getsizeof(d)} B")
print(f"  id(d)               : 0x{id(d):016x}")
print(f"  ma_keys 주소        : 0x{get_ma_keys_addr(d):016x}")
print()

# 항목 추가 전후 id(d) 비교
prev_id = id(d)
for k in ["a", "b", "c", "d", "e"]:
    d[k] = k
    current_id = id(d)
    moved = "" if current_id == prev_id else " [moved?!]"
    print(f"  d['{k}'] 추가 후  id(d) = 0x{current_id:016x}{moved}"
          f"  size={sys.getsizeof(d)} B")

print()
print("  결론:")
print("    id(d) -- 항목을 추가해도 딕셔너리 오브젝트 주소는 변하지 않는다.")
print("    ma_keys -- 항목 증가에 따라 새 버킷 배열로 교체될 수 있다.")
print("    sys.getsizeof(d) -- dict 오브젝트 헤더만 측정; 버킷 배열은 별도 할당.")
print()

# 크기 변화 추적
print("  항목 수에 따른 sys.getsizeof(d) 변화:")
d2 = {}
prev_size = sys.getsizeof(d2)
print(f"    항목 0개 : {prev_size} B")
for i in range(1, 13):
    d2[i] = i
    sz = sys.getsizeof(d2)
    note = " [크기 변화]" if sz != prev_size else ""
    print(f"    항목 {i:>2}개 : {sz} B{note}")
    prev_size = sz
print()
