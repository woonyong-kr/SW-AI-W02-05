#!/usr/bin/env python3
"""
알고리즘 벤치마크 비교 스크립트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
그래프 구조: 5-ary 트리 (분기 계수 B = 5)
  레벨 0 : 1개   (루트)
  레벨 1 : 5개
  레벨 2 : 25개
  레벨 k : 5^k 개
  레벨 7 : 78,125개  →  총 (5^8-1)/4 = 97,656개 노드

노드 번호 규칙
  루트   = 0
  parent(nid) = (nid - 1) // 5
  children(nid) = [5*nid+1, 5*nid+2, 5*nid+3, 5*nid+4, 5*nid+5]  (< TOTAL)

목표 노드: 97,655 (레벨 7, 최우측 리프)
  최단 경로: 0 → 5 → 30 → 155 → 780 → 3905 → 19530 → 97655  (7홉)

대상 알고리즘 (ex/ 원본 로직 기반, 계측 코드 추가)
  BFS · DFS · Dijkstra · A* · Greedy Best-First · IDDFS

계측 항목
  실행 시간(μs)  ·  피크 메모리(KB)  ·  탐색 노드 수
  자료구조 최대 크기  ·  총 삽입/푸시 횟수
  tracemalloc 라인별 할당 분석 (Python 객체 생성 원인)
"""

import sys, time, tracemalloc, heapq, math
from collections import deque

# ══════════════════════════════════════════════════════════════════════════
# ANSI 컬러
# ══════════════════════════════════════════════════════════════════════════
BOLD    = '\033[1m'
DIM     = '\033[2m'
RESET   = '\033[0m'
GREEN   = '\033[92m'
CYAN    = '\033[96m'
YELLOW  = '\033[93m'
RED     = '\033[91m'
BLUE    = '\033[94m'
MAGENTA = '\033[95m'
WHITE   = '\033[97m'

# ══════════════════════════════════════════════════════════════════════════
# 1. 5-ary 트리 구성
# ══════════════════════════════════════════════════════════════════════════
B      = 5                                          # 분기 계수
LEVELS = 7                                          # 최대 레벨 (0 ~ 7)
TOTAL  = (B ** (LEVELS + 1) - 1) // (B - 1)        # 97,656 노드
START  = 0
GOAL   = TOTAL - 1                                  # 97,655 (최우측 리프)


def level_of(nid: int) -> int:
    """nid가 속한 레벨 반환 (루트=0)"""
    if nid == 0:
        return 0
    # 레벨 L의 첫 번째 노드 인덱스 = (B^L - 1) / (B-1)
    # nid >= first_of_level  →  floor(log_B(nid*(B-1)+1))
    return math.floor(math.log(nid * (B - 1) + 1, B))


# ── 인접 리스트 구성
#    자식을 내림차순(5→1)으로 저장
#    → DFS에서 reversed(ADJ[n]) 호출 시 rightmost 자식이 스택 TOP에 위치
#    → 목표(최우측 리프)를 DFS가 단 8번 방문으로 즉시 발견
print(f'\n  {DIM}그래프 구성 중 (B={B}, LEVELS={LEVELS}, 총 {TOTAL:,} 노드)...{RESET}',
      end='', flush=True)

ADJ: list[list[int]] = [[] for _ in range(TOTAL)]
for nid in range(TOTAL):
    # 자식 추가 (내림차순: child_B → child_1)
    for c in range(B, 0, -1):
        child = B * nid + c
        if child < TOTAL:
            ADJ[nid].append(child)
    # 부모 추가 (루트 제외)
    if nid > 0:
        ADJ[nid].append((nid - 1) // B)

print(f' {GREEN}완료{RESET}')

# ── 목표까지의 최단 경로 (검증용)
_path: list[int] = []
_n = GOAL
while _n != START:
    _path.append(_n)
    _n = (_n - 1) // B
_path.append(START)
_path.reverse()
PATH_TO_GOAL   = _path
SHORTEST_HOPS  = len(PATH_TO_GOAL) - 1   # = LEVELS = 7


# ══════════════════════════════════════════════════════════════════════════
# 2. 휴리스틱 함수 (A* · Greedy 공용)
#    h(n) = 목표 레벨 - 현재 레벨
#    • 허용 가능(admissible): 실제 거리 ≥ 레벨 차이
#    • 단, 분기 선택 정보 없음 → A* 성능이 Dijkstra와 유사
# ══════════════════════════════════════════════════════════════════════════
def heuristic(nid: int) -> int:
    return LEVELS - level_of(nid)


# ══════════════════════════════════════════════════════════════════════════
# 3. 계측 함수  (ex/ 원본 로직 + 메트릭 수집)
# ══════════════════════════════════════════════════════════════════════════

# ── BFS  (ex/bfs.py 기반)
def bench_bfs():
    visited     = {START}
    queue       = deque([START])
    visit_count = 0
    ds_max      = 1
    ds_total    = 1

    while queue:
        curr = queue.popleft()
        visit_count += 1
        if curr == GOAL:
            break
        for nb in ADJ[curr]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                ds_total += 1
                if len(queue) > ds_max:
                    ds_max = len(queue)

    return dict(
        found        = (curr == GOAL),
        visit_count  = visit_count,
        ds_max       = ds_max,
        ds_total     = ds_total,
        ds_name      = '큐 (deque)',
        ds_max_label = '큐 최대 크기',
        extra        = f'총 enqueue {ds_total:,}회',
    )


# ── DFS  (ex/dfs.py  dfs_iterative 기반)
#    ADJ 자식이 내림차순 → reversed() 후 rightmost 자식이 스택 TOP
#    → 최우측 경로(0→5→30→…→97655)를 첫 번째로 탐색, 8번 방문으로 목표 발견
def bench_dfs():
    visited     = set()
    stack       = [START]
    visit_count = 0
    ds_max      = 1
    ds_total    = 1

    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        visit_count += 1
        if curr == GOAL:
            break
        for nb in reversed(ADJ[curr]):
            if nb not in visited:
                stack.append(nb)
                ds_total += 1
                if len(stack) > ds_max:
                    ds_max = len(stack)

    return dict(
        found        = (curr == GOAL),
        visit_count  = visit_count,
        ds_max       = ds_max,
        ds_total     = ds_total,
        ds_name      = '스택 (list)',
        ds_max_label = '스택 최대 크기',
        extra        = f'총 push {ds_total:,}회',
    )


# ── Dijkstra  (ex/dijkstra.py 기반)
#    ★ 핵심: distances = {n: float('inf') for n in range(TOTAL)}
#      → 97,656개 float 객체를 탐색 시작 전에 즉시(Eager) 생성
#      → BFS/DFS 대비 메모리 수십 배 차이의 원인
def bench_dijkstra():
    distances         = {n: float('inf') for n in range(TOTAL)}   # ← 전체 사전 할당
    distances[START]  = 0
    pq          = [(0, START)]
    visit_count = 0
    ds_max      = 1
    ds_total    = 1

    while pq:
        curr_dist, curr = heapq.heappop(pq)
        if curr_dist > distances[curr]:
            continue
        visit_count += 1
        if curr == GOAL:
            break
        for nb in ADJ[curr]:
            # 모든 엣지 weight = 1
            if nb == (curr - 1) // B or any(B * curr + c == nb for c in range(1, B + 1)):
                w = 1
            else:
                w = 1
            d = curr_dist + 1   # 균일 가중치
            if d < distances[nb]:
                distances[nb] = d
                heapq.heappush(pq, (d, nb))
                ds_total += 1
                if len(pq) > ds_max:
                    ds_max = len(pq)

    return dict(
        found        = (distances[GOAL] < float('inf')),
        visit_count  = visit_count,
        ds_max       = ds_max,
        ds_total     = ds_total,
        ds_name      = '우선순위 큐 (heapq)',
        ds_max_label = '힙 최대 크기',
        extra        = f'목표 dist={distances[GOAL]:.0f}',
        _distances   = distances,   # 크기 분석용 (표 출력 제외)
    )


# ── A*  (ex/a_star.py 기반)
#    ★ 핵심: g_score + f_score 두 개의 사전 할당
#      → Dijkstra의 2배 메모리 (97,656 float × 2 = 195,312 객체)
#      → h(n)=레벨 기반이므로 f = g + h = level + (7-level) = 7 (모든 노드 동일)
#      → 사실상 BFS와 동일한 탐색 순서, 메모리만 더 사용
def bench_a_star():
    g_score           = {n: float('inf') for n in range(TOTAL)}   # ← 사전 할당 ①
    f_score           = {n: float('inf') for n in range(TOTAL)}   # ← 사전 할당 ②
    g_score[START]    = 0
    f_score[START]    = heuristic(START)
    pq          = [(f_score[START], START)]
    visit_count = 0
    ds_max      = 1
    ds_total    = 1
    found       = False

    while pq:
        _, curr = heapq.heappop(pq)
        visit_count += 1
        if curr == GOAL:
            found = True
            break
        for nb in ADJ[curr]:
            tg = g_score[curr] + 1   # 균일 가중치
            if tg < g_score[nb]:
                g_score[nb] = tg
                f = tg + heuristic(nb)
                f_score[nb] = f
                heapq.heappush(pq, (f, nb))
                ds_total += 1
                if len(pq) > ds_max:
                    ds_max = len(pq)

    return dict(
        found        = found,
        visit_count  = visit_count,
        ds_max       = ds_max,
        ds_total     = ds_total,
        ds_name      = '우선순위 큐 (heapq)',
        ds_max_label = '힙 최대 크기',
        extra        = f'목표 dist={g_score[GOAL]:.0f}, h=레벨 기반',
        _g_score     = g_score,
        _f_score     = f_score,
    )


# ── Greedy Best-First  (ex/greedy.py 기반)
#    h(n)만 사용, 실제 비용 무시
#    동점(같은 레벨) → node_id 오름차순으로 팝 → 좌측 우선 탐색
#    → 최우측 목표(97655)를 찾기까지 대부분 노드 방문
def bench_greedy():
    visited     = set()
    pq          = [(heuristic(START), START)]
    visit_count = 0
    ds_max      = 1
    ds_total    = 1
    found       = False

    while pq:
        _, curr = heapq.heappop(pq)
        if curr == GOAL:
            found        = True
            visit_count += 1
            break
        if curr not in visited:
            visited.add(curr)
            visit_count += 1
            for nb in ADJ[curr]:
                if nb not in visited:
                    heapq.heappush(pq, (heuristic(nb), nb))
                    ds_total += 1
                    if len(pq) > ds_max:
                        ds_max = len(pq)

    return dict(
        found        = found,
        visit_count  = visit_count,
        ds_max       = ds_max,
        ds_total     = ds_total,
        ds_name      = '우선순위 큐 (heapq)',
        ds_max_label = '힙 최대 크기',
        extra        = 'h(n)=레벨 기반, 실제 비용 무시',
    )


# ── IDDFS  (ex/iddfs.py 기반)
#    ★ 핵심: path_set은 현재 경로의 노드만 포함 (최대 LEVELS+1 = 8개)
#      → 메모리 극소, 대신 낮은 깊이를 반복 재탐색
#    ADJ 자식 내림차순 → 깊이 7 반복에서 최우측 경로를 첫 번째로 시도
#    → DLS 호출 8회로 즉시 목표 발견 (하지만 이전 깊이 누적 호출이 존재)
def bench_iddfs():
    counter  = {'visits': 0, 'dls_calls': 0, 'max_depth': 0}
    found_at = None

    def dls(node: int, limit: int, depth: int, path_set: set) -> bool:
        counter['dls_calls'] += 1
        counter['visits']    += 1
        if depth > counter['max_depth']:
            counter['max_depth'] = depth
        if node == GOAL:
            return True
        if limit <= 0:
            return False
        path_set.add(node)
        for nb in ADJ[node]:
            if nb not in path_set:
                if dls(nb, limit - 1, depth + 1, path_set):
                    return True
        path_set.remove(node)   # 백트래킹: 다른 경로에서 재방문 허용
        return False

    for depth_limit in range(LEVELS + 1):
        if dls(START, depth_limit, 0, set()):
            found_at = depth_limit
            break

    return dict(
        found        = (found_at is not None),
        visit_count  = counter['visits'],
        ds_max       = counter['max_depth'],
        ds_total     = counter['dls_calls'],
        ds_name      = '콜 스택 (재귀)',
        ds_max_label = '최대 재귀 깊이',
        extra        = f'발견 깊이={found_at}, 총 DLS호출={counter["dls_calls"]:,}',
        found_depth  = found_at,
        dls_calls    = counter['dls_calls'],
    )


# ══════════════════════════════════════════════════════════════════════════
# 4. 계측 래퍼  (시간 + tracemalloc 피크 + 스냅샷)
# ══════════════════════════════════════════════════════════════════════════
def measure(fn):
    tracemalloc.start()
    snap1      = tracemalloc.take_snapshot()
    t0         = time.perf_counter_ns()
    result     = fn()
    elapsed_ns = time.perf_counter_ns() - t0
    snap2      = tracemalloc.take_snapshot()
    _, peak    = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result['time_us'] = elapsed_ns / 1_000
    result['mem_kb']  = peak / 1_024
    result['_snap1']  = snap1
    result['_snap2']  = snap2
    return result


# ══════════════════════════════════════════════════════════════════════════
# 5. 출력 함수
# ══════════════════════════════════════════════════════════════════════════
ALGO_COLORS = {
    'BFS':      CYAN,
    'DFS':      YELLOW,
    'Dijkstra': MAGENTA,
    'A*':       GREEN,
    'Greedy':   BLUE,
    'IDDFS':    RED,
}

def bar(value: float, max_val: float, width: int = 18) -> str:
    ratio  = min(value / max_val, 1.0) if max_val else 0
    filled = round(ratio * width)
    b = '█' * filled + '░' * (width - filled)
    color = GREEN if ratio < 0.34 else (YELLOW if ratio < 0.67 else RED)
    return f'{color}{b}{RESET}'


def print_graph_summary():
    W = 92
    print(f'\n{BOLD}{CYAN}{"━" * W}{RESET}')
    print(f'{BOLD}{CYAN}  5-ary 트리 구조 요약  (B={B}, LEVELS={LEVELS}){RESET}')
    print(f'{BOLD}{CYAN}{"━" * W}{RESET}')
    print(f'{DIM}  {"레벨":^5} {"노드수":^10} {"누적 합계":^12} {"레벨 첫 노드 ID":^16} 비고{RESET}')
    print(f'  {"─" * (W - 2)}')
    cumul = 0
    for lv in range(LEVELS + 1):
        count  = B ** lv
        cumul += count
        first  = (B ** lv - 1) // (B - 1)
        note   = ' ← START (루트)' if lv == 0 else ''
        note   = f' ← {GREEN}GOAL = {GOAL}{RESET}' if lv == LEVELS else note
        print(f'  {lv:^5} {count:^10,} {cumul:^12,} {first:^16,}{note}')
    print(f'  {"─" * (W - 2)}')
    total_edges = sum(len(v) for v in ADJ) // 2
    print(f'  총 노드: {BOLD}{TOTAL:,}{RESET}   총 엣지: {BOLD}{total_edges:,}{RESET}'
          f'   최단 경로: {BOLD}{SHORTEST_HOPS}{RESET}홉')
    path_str = ' → '.join(str(n) for n in PATH_TO_GOAL)
    print(f'  경로: {DIM}{path_str}{RESET}\n')


def print_table(results: dict):
    W = 92
    max_time = max(r['time_us']     for r in results.values())
    max_mem  = max(r['mem_kb']      for r in results.values())
    max_vis  = max(r['visit_count'] for r in results.values())
    max_ds   = max(r['ds_max']      for r in results.values())
    max_push = max(r['ds_total']    for r in results.values())

    SEP   = f'{DIM}{"─" * W}{RESET}'
    THICK = f'{BOLD}{CYAN}{"═" * W}{RESET}'

    print(THICK)
    print(f'{BOLD}{CYAN}  알고리즘 벤치마크 결과  '
          f'(5-ary 트리, {TOTAL:,}노드, 목표={GOAL}){RESET}')
    print(THICK)
    print(f'{BOLD}  {"알고리즘":<12} {"시간(μs)":>10} {"메모리(KB)":>11}'
          f' {"탐색 노드":>10} {"구조 최대":>10} {"총 삽입":>10}  자료구조{RESET}')
    print(SEP)

    for name, r in results.items():
        c     = ALGO_COLORS.get(name, RESET)
        found = f'{GREEN}✅{RESET}' if r['found'] else f'{RED}❌{RESET}'
        print(
            f'  {c}{BOLD}{name:<12}{RESET}'
            f' {r["time_us"]:>10.1f}'
            f' {r["mem_kb"]:>11.2f}'
            f' {r["visit_count"]:>10,}'
            f' {r["ds_max"]:>10,}'
            f' {r["ds_total"]:>10,}'
            f'  {DIM}{r["ds_name"]}{RESET}'
            f'  {found}'
        )
    print(SEP)

    # 세부 결과
    print(f'\n{BOLD}  ▶ 세부 결과{RESET}')
    for name, r in results.items():
        c = ALGO_COLORS.get(name, RESET)
        print(f'    {c}{BOLD}{name:<10}{RESET} {DIM}{r["extra"]}{RESET}')

    # 막대 그래프
    print(f'\n{BOLD}  ▶ 시각적 비교{RESET}')
    sections = [
        ('[시간]  연산 시간 (us)',     'time_us',     max_time,  '.1f'),
        ('[탐색] 탐색 노드 수',        'visit_count', max_vis,   ',d'),
        ('[메모리] 피크 메모리 (KB)',  'mem_kb',      max_mem,   '.2f'),
        ('[구조] 자료구조 최대 크기',  'ds_max',      max_ds,    ',d'),
        ('[삽입] 총 삽입/푸시 횟수',   'ds_total',    max_push,  ',d'),
    ]
    for title, key, mx, fmt in sections:
        print(f'\n  {BOLD}{title}{RESET}')
        for name, r in results.items():
            c       = ALGO_COLORS.get(name, RESET)
            val     = r[key]
            fmt_str = f'{val:{fmt}}'
            lbl     = f'({r["ds_max_label"]})' if key == 'ds_max' else ''
            print(f'    {c}{name:<10}{RESET} {bar(val, mx)}  {fmt_str} {DIM}{lbl}{RESET}')

    # IDDFS 심층 분석
    if 'IDDFS' in results:
        r = results['IDDFS']
        print(f'\n{BOLD}  ▶ IDDFS 심층 분석{RESET}')
        fd = r.get('found_depth')
        dc = r.get('dls_calls', 0)
        print(f'    발견 깊이        : {fd}  (전체 {LEVELS} 레벨 트리)')
        print(f'    총 DLS 호출 수   : {dc:,}')
        print(f'      {DIM}깊이 0~{fd-1} 반복 탐색 누적  +  깊이 {fd} 첫 경로에서 즉시 발견{RESET}')
        if fd is not None and fd > 0:
            # 이전 깊이까지 누적 호출 수 계산
            prev = sum((B**(d+1) - 1) // (B - 1) for d in range(fd))
            final = dc - prev
            print(f'      깊이 0~{fd-1} 합산  : {prev:,}회')
            print(f'      깊이 {fd} (발견)    : {final:,}회  ← 최우측 경로 첫 시도에서 발견')
        print(f'    최대 재귀 깊이   : {r["ds_max"]}  {DIM}(Python 콜 스택 프레임){RESET}')

    # 요약 인사이트
    fastest  = min(results, key=lambda n: results[n]['time_us'])
    smallest = min(results, key=lambda n: results[n]['visit_count'])
    lowest   = min(results, key=lambda n: results[n]['mem_kb'])
    print(f'\n{BOLD}  ▶ 요약 인사이트{RESET}')
    print(f'    {GREEN}가장 빠름{RESET}         : {BOLD}{fastest}{RESET}'
          f'  ({results[fastest]["time_us"]:.1f} μs)')
    print(f'    {GREEN}탐색 노드 최소{RESET}    : {BOLD}{smallest}{RESET}'
          f'  ({results[smallest]["visit_count"]:,}개)')
    print(f'    {GREEN}메모리 최소{RESET}       : {BOLD}{lowest}{RESET}'
          f'  ({results[lowest]["mem_kb"]:.2f} KB)')
    print(f'\n{THICK}\n')


# ══════════════════════════════════════════════════════════════════════════
# 6. 메모리 심층 분석
#    (A) tracemalloc 라인별 할당 diff  → "어디서 Python 객체가 더 생성되는지"
#    (B) 핵심 자료구조 sys.getsizeof 비교
#    (C) 알고리즘별 메모리 패턴 해설
# ══════════════════════════════════════════════════════════════════════════
def print_memory_analysis(results: dict):
    W = 92
    THICK = f'{BOLD}{CYAN}{"═" * W}{RESET}'
    SEP   = f'{DIM}{"─" * W}{RESET}'

    print(f'\n{THICK}')
    print(f'{BOLD}{CYAN}  메모리 심층 분석  -- Python 객체 생성 원인 분석{RESET}')
    print(THICK)

    # ── (A) tracemalloc 라인별 diff
    print(f'\n{BOLD}  ▶ (A) tracemalloc 라인별 메모리 할당 TOP 5{RESET}')
    print(f'  {DIM}snap_before → snap_after  |  알고리즘 실행 구간만 계측{RESET}\n')

    for name, r in results.items():
        if '_snap1' not in r or '_snap2' not in r:
            continue
        c = ALGO_COLORS.get(name, RESET)
        print(f'  {c}{BOLD}[ {name} ]{RESET}')
        stats  = r['_snap2'].compare_to(r['_snap1'], 'lineno')
        shown  = 0
        for stat in stats:
            if stat.size_diff <= 0:
                continue
            tb      = stat.traceback[0]
            fname   = tb.filename
            # 긴 경로 단축
            for prefix in [
                '/sessions/nifty-cool-thompson/mnt/SW-AI-W02-05/',
                '/sessions/nifty-cool-thompson/',
            ]:
                fname = fname.replace(prefix, '')
            lineno  = tb.lineno
            kb_diff = stat.size_diff / 1_024
            cnt     = stat.count_diff
            bar_w   = min(int(kb_diff / 100), 20)
            bstr    = '▓' * bar_w
            print(f'    L{lineno:>5}  {kb_diff:>9.2f} KB  {cnt:>+8,} 객체  '
                  f'{CYAN}{bstr}{RESET}  {DIM}{fname}{RESET}')
            shown += 1
            if shown >= 5:
                break
        if shown == 0:
            print(f'    {DIM}(유의미한 신규 할당 없음){RESET}')
        print()

    # ── (B) 핵심 자료구조 sys.getsizeof
    print(SEP)
    print(f'\n{BOLD}  ▶ (B) 핵심 자료구조 sys.getsizeof{RESET}')
    print(f'  {DIM}shallow = dict/list/set 객체 자체 크기 (내부 값 객체 미포함){RESET}')
    print(f'  {DIM}deep_est = 값 객체 포함 추정치  (float 하나 = 24 B in CPython){RESET}\n')

    FLOAT_BYTES = 24   # CPython float 객체 크기

    def show_struct(label: str, obj, color: str = WHITE, extra: str = ''):
        shallow  = sys.getsizeof(obj)
        n        = len(obj)
        deep_est = shallow + n * FLOAT_BYTES   # 값이 float인 dict 추정
        print(f'    {color}{BOLD}{label:<36}{RESET}'
              f'  항목 수={n:>7,}'
              f'  shallow={shallow:>9,} B'
              f'  deep_est≈{deep_est/1024:>7.1f} KB'
              f'  {DIM}{extra}{RESET}')

    dij_r   = results.get('Dijkstra', {})
    astar_r = results.get('A*', {})

    if '_distances' in dij_r:
        show_struct('Dijkstra  distances dict',
                    dij_r['_distances'], MAGENTA,
                    '← 탐색 전 전체 노드 inf 사전 할당')
    if '_g_score' in astar_r:
        show_struct('A*  g_score dict',
                    astar_r['_g_score'], GREEN,
                    '← 사전 할당 ①')
        show_struct('A*  f_score dict',
                    astar_r['_f_score'], GREEN,
                    '← 사전 할당 ②')
        g_shallow = sys.getsizeof(astar_r['_g_score'])
        f_shallow = sys.getsizeof(astar_r['_f_score'])
        n         = len(astar_r['_g_score'])
        total_est = g_shallow + f_shallow + n * 2 * FLOAT_BYTES
        print(f'    {GREEN}{BOLD}{"A*  합계 (g + f)":<36}{RESET}'
              f'  {"":>15}'
              f'  {"":>18}'
              f'  deep_est≈{total_est/1024:>7.1f} KB'
              f'  {DIM}Dijkstra × 2{RESET}')

    print(f'\n    {DIM}BFS/DFS/Greedy : visited set + 큐/스택은 탐색 진행에 따라 점진적 성장{RESET}')
    print(f'    {DIM}IDDFS          : path_set은 현재 경로 노드만 (최대 {LEVELS+1}개 ≈ 수십 B){RESET}')

    # ── (C) 알고리즘별 메모리 패턴 해설
    print(f'\n{SEP}')
    print(f'\n{BOLD}  ▶ (C) 알고리즘별 메모리 패턴 해설{RESET}')
    print()

    patterns = [
        ('BFS', CYAN,
         '지연(Lazy) 할당',
         'visited set + deque가 탐색 노드 수에 비례하여 점진적 증가',
         f'최우측 목표 → 모든 {TOTAL:,}개 노드 방문 → visited/queue 최대 크기'),

        ('DFS', YELLOW,
         '지연(Lazy) 할당  +  우측 우선 탐색',
         '스택·visited 모두 지연 할당  /  ADJ 내림차순 → reversed() → 우측 자식 TOP',
         f'0→5→30→…→{GOAL} 경로만 탐색, 단 {SHORTEST_HOPS+1}회 방문 → 메모리 극소'),

        ('Dijkstra', MAGENTA,
         '즉시(Eager) 전체 사전 할당',
         'distances = {n: float("inf") for n in range(TOTAL)}'
         f'  →  {TOTAL:,}개 float 객체 즉시 생성',
         f'약 {TOTAL * FLOAT_BYTES // 1024} KB  (BFS visited set이 {SHORTEST_HOPS+1}개일 때와 비교)'),

        ('A*', GREEN,
         '즉시(Eager) 사전 할당 × 2  (g_score + f_score)',
         f'g_score + f_score 각각 {TOTAL:,}개 float 선할당  =  Dijkstra × 2',
         f'h(n)=레벨 차이 → f = level + (7-level) = 7 (동일) → BFS와 같은 탐색 순서'),

        ('Greedy', BLUE,
         '지연(Lazy) 할당',
         'visited set + heapq만 사용, 사전 할당 없음',
         '동점 시 node_id 오름차순(좌측 우선) → 최우측 목표 탐색에 불리, 대부분 노드 방문'),

        ('IDDFS', RED,
         '경로 전용 집합 (백트래킹)',
         f'path_set = 현재 DLS 경로의 노드만 (최대 {LEVELS+1}개, 백트래킹 시 즉시 제거)',
         '메모리 최소  /  대신 이전 깊이 반복 재탐색으로 총 DLS 호출 증가'),
    ]

    for name, color, pattern, detail, note in patterns:
        if name not in results:
            continue
        r = results[name]
        print(f'  {color}{BOLD}{name}{RESET}  {DIM}[{pattern}]{RESET}')
        print(f'    {detail}')
        print(f'    {DIM}→ {note}{RESET}')
        print(f'    피크 메모리: {BOLD}{r["mem_kb"]:.2f} KB{RESET}'
              f'   탐색 노드: {BOLD}{r["visit_count"]:,}{RESET}\n')

    print(THICK)
    print(f'\n{BOLD}  ▶ 핵심 정리{RESET}')
    print(f'''
  {MAGENTA}{BOLD}Dijkstra/A*{RESET} : 탐색 시작 전 모든 노드에 대한 distances/g_score/f_score를
              dict comprehension으로 즉시 생성 → 노드 수에 비례한 대용량 할당
              → 코드 한 줄({MAGENTA}{{n: float("inf") for n in range(TOTAL)}}{RESET})이
                 {TOTAL:,}개 Python 객체를 생성하는 원인

  {CYAN}{BOLD}BFS/DFS/Greedy{RESET}: 사전 할당 없음, 방문하는 노드만 set/queue/heap에 추가
              → 탐색 범위가 좁으면 메모리도 적게 사용 (DFS: 8개 방문)

  {RED}{BOLD}IDDFS{RESET}          : path_set에 현재 경로 노드만 보관 + 백트래킹 즉시 제거
              → 메모리 O(depth) = 가장 메모리 효율적, 시간은 반복 탐색 비용
''')


# ══════════════════════════════════════════════════════════════════════════
# 실행
# ══════════════════════════════════════════════════════════════════════════
BENCHMARKS = [
    ('BFS',      bench_bfs),
    ('DFS',      bench_dfs),
    ('Dijkstra', bench_dijkstra),
    ('A*',       bench_a_star),
    ('Greedy',   bench_greedy),
    ('IDDFS',    bench_iddfs),
]

if __name__ == '__main__':
    print_graph_summary()

    print(f'{BOLD}  ▌ 계측 시작 (각 알고리즘 1회 실행){RESET}\n')
    results: dict = {}
    for name, fn in BENCHMARKS:
        c = ALGO_COLORS.get(name, RESET)
        sys.stdout.write(f'  {c}{BOLD}{name:<10}{RESET} 실행 중... ')
        sys.stdout.flush()
        results[name] = measure(fn)
        r      = results[name]
        status = f'{GREEN}완료{RESET}' if r['found'] else f'{RED}미발견{RESET}'
        print(f'{status}'
              f'  ({r["time_us"]:,.1f} μs'
              f'  /  {r["mem_kb"]:.2f} KB'
              f'  /  탐색 {r["visit_count"]:,}노드)')

    print()
    print_table(results)
    print_memory_analysis(results)
