"""
[01] Dummy 클래스 기본 메모리 크기
────────────────────────────────────────────────────────────────
확인 항목
    - 아무것도 없는 클래스 인스턴스가 차지하는 메모리
    - __slots__ 사용 시 차이
    - CPython 인스턴스 구성 분해
"""

import sys

SEP = "-" * 60


# ── 더미 클래스 ───────────────────────────────────────────────────
class Dummy:
    """속성, 메서드, 슬롯 아무것도 없는 빈 클래스."""
    pass


class DummySlots:
    """__slots__ 로 __dict__ 를 제거한 최소 클래스."""
    __slots__ = ()


# ── 실행 ─────────────────────────────────────────────────────────
d_normal = Dummy()
d_slots  = DummySlots()

print(SEP)
print("[01] Dummy 클래스 기본 메모리 크기")
print(SEP)

print()
print(f"  sys.getsizeof(object())      = {sys.getsizeof(object()):>3} B  <- Python 최소 오브젝트")
print(f"  sys.getsizeof(Dummy())       = {sys.getsizeof(d_normal):>3} B  <- 일반 클래스 인스턴스")
print(f"  sys.getsizeof(DummySlots())  = {sys.getsizeof(d_slots):>3} B  <- __slots__ 사용 시")

print()
print("  Dummy() 구성 (CPython 64비트):")
print("      ob_refcnt   8 B  참조 카운터")
print("      ob_type     8 B  타입 포인터")
print("      __dict__    8 B  인스턴스 속성 딕셔너리 포인터")
print("      __weakref__ 8 B  약참조 지원 포인터")
print(f"      합계       32 B  (헤더 포함 실제 {sys.getsizeof(d_normal)} B)")

print()
print("  DummySlots() 는 __dict__ 와 __weakref__ 가 없으므로")
print(f"  {sys.getsizeof(d_slots)} B 로 줄어든다.")
print()
