"""
demo_array_search.py — 선형 탐색 vs 이진 탐색
==============================================
실행:
    cd week4/bfs-dfs
    python3 demo_array_search.py

문제 정의
---------
16개의 값이 담긴 배열에서 특정 값을 찾는다.

    선형 탐색 (Linear Search)
        - 정렬 여부 무관
        - 처음부터 순서대로 비교
        - 최악 O(n), 평균 O(n/2)

    이진 탐색 (Binary Search)
        - 정렬된 배열에서만 가능
        - 중앙값과 비교 후 탐색 범위를 절반으로 줄임
        - O(log n)

데모는 두 탐색을 같은 값에 대해 순서대로 실행한다.
R 키를 누를 때마다: 선형 탐색 → 이진 탐색 → 선형 탐색 → ...

키보드
------
    SPACE    : 일시정지 / 재개
    UP / DOWN: 속도 조절
    R        : 재시작 (다음 탐색 방식으로 전환)
    Q        : 종료
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Array1D

# ── 배열 데이터 (고정 시드) ────────────────────────────────────────────
_SORTED_DATA = [3, 7, 12, 18, 24, 31, 39, 45, 52, 60, 67, 73, 81, 88, 94, 99]
_TARGET = 67       # 인덱스 10 에 있음 (이진 탐색: 4스텝, 선형: 11스텝)


# ─────────────────────────────────────────────────────────────────────────────
# 선형 탐색
# ─────────────────────────────────────────────────────────────────────────────

class LinearSearchDemo(Scene):
    """
    선형 탐색 시각화.
    배열을 처음부터 순서대로 검사한다.
    """

    def setup(self):
        a = Array1D(len(_SORTED_DATA), wrap_cols=8)
        self.use(a)

        for i, v in enumerate(_SORTED_DATA):
            self.label(i, str(v))

        self.section("선형 탐색  O(n)")
        self.info("배열 크기", len(_SORTED_DATA))
        self.info("찾는 값",   str(_TARGET))
        self.section("색상 범례")
        self.info("노란색",   "현재 검사 중")
        self.info("파란색",   "검사 완료 (불일치)")
        self.info("초록색",   "발견!")

    def solve(self):
        data   = _SORTED_DATA
        target = _TARGET

        for i in range(len(data)):
            self.frontier(i)          # 현재 검사 중
            yield

            if data[i] == target:
                self.mark(i, "start") # 발견
                return

            self.visit(i)             # 불일치 → 방문 처리


# ─────────────────────────────────────────────────────────────────────────────
# 이진 탐색
# ─────────────────────────────────────────────────────────────────────────────

class BinarySearchDemo(Scene):
    """
    이진 탐색 시각화.
    정렬된 배열에서 중앙값과 비교하며 탐색 범위를 절반씩 줄인다.

    색상 의미
    ---------
    wall (어두운색) : 이미 제외된 탐색 범위
    frontier (노란색): 현재 검사 중인 중앙값
    visited (파란색) : 탐색 범위 안에 있는 후보
    start (초록색)   : 발견된 위치
    """

    def setup(self):
        a = Array1D(len(_SORTED_DATA), wrap_cols=8)
        self.use(a)

        for i, v in enumerate(_SORTED_DATA):
            self.label(i, str(v))

        self.section("이진 탐색  O(log n)")
        self.info("배열 크기", len(_SORTED_DATA))
        self.info("찾는 값",   str(_TARGET))
        self.section("색상 범례")
        self.info("노란색",   "현재 검사 (mid)")
        self.info("파란색",   "탐색 범위 후보")
        self.info("어두운색", "제외된 범위")
        self.info("초록색",   "발견!")

    def solve(self):
        data   = _SORTED_DATA
        target = _TARGET
        lo, hi = 0, len(data) - 1

        # 초기 탐색 범위를 frontier 로 표시
        for i in range(lo, hi + 1):
            self.visit(i)

        while lo <= hi:
            mid = (lo + hi) // 2

            self.frontier(mid)        # 현재 중앙값 강조
            yield

            if data[mid] == target:
                self.mark(mid, "start")
                return

            elif data[mid] < target:
                # 왼쪽 절반 제외
                for i in range(lo, mid + 1):
                    self.wall(i)
                lo = mid + 1

            else:
                # 오른쪽 절반 제외
                for i in range(mid, hi + 1):
                    self.wall(i)
                hi = mid - 1

            # 남은 탐색 범위 재표시
            for i in range(lo, hi + 1):
                self.visit(i)

            yield


# ─────────────────────────────────────────────────────────────────────────────
# 실행 — 두 탐색을 교대로 실행
# ─────────────────────────────────────────────────────────────────────────────

import sys

_DEMOS = [LinearSearchDemo, BinarySearchDemo]
_TITLES = [
    "선형 탐색 — Linear Search  O(n)",
    "이진 탐색 — Binary Search  O(log n)",
]
_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0

_DEMOS[_idx % 2]().run(_TITLES[_idx % 2], config_path="vizlib.json")
