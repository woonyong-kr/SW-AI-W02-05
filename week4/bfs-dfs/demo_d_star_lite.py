"""
demo_d_star_lite.py — D* Lite (Dynamic A*) 개념 증명 시각화
===================================================

경로를 순항하던 중, 로봇의 센서에 미리 알지 못했던 새로운 장애물(벽)이 감지되었을 때!
A* 처럼 출발점부터 다시 수백만 타일을 재탐색하지 않고, 
"충돌한 그 위치周辺"만 국소적으로 뒤집어(RHS 값 업데이트) 재빠르게 경로를 복구하는 D* 의 연출입니다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vizlib import Scene, Grid2D
from vizlib.tracer import Tracer

class DStarDemo(Scene):
    def setup(self):
        g = Grid2D(25, 25)
        self.use(g)
        self.start((2, 2))
        self.end((22, 22))
        self.section("D* Lite (동적 환경 알고리즘)")
        self.info("배경", "게임 플레이 중 유저가 건물을 지어 원래 있던 길이 갑자기 막힘!")
        self.info("특징", "막힌 지점 근처의 가중치만 국지적으로 업데이트하여 즉시 우회")

    def solve(self):
        tracer = Tracer()
        
        # 1. 초기 계산된 완벽한 대각선 경로 (A* 가 미리 짜준 길)
        route_initial = [(r, r) for r in range(2, 12)]
        
        tracer.info("로봇 상태", "최초 경로를 따라 순항 중...")
        for p in route_initial:
            tracer.color(p, (100, 200, 255))
            tracer.label(p, "로봇")
            tracer.log_step()
            tracer.label(p, "")
            tracer.visit(p)
            
        # 돌발 상황: 시야(센서)에 새로운 거대 장애물 발견
        tracer.info("로봇 상태", "센서 경고! 경로 전방에 예상치 못한 거대 장애물 감지!")
        tracer.log_step()
        for i in range(12, 18):
            for j in range(12, 14):
                tracer.color((i, j), (220, 40, 40)) # 붉은 벽
                tracer.label((i, j), "WALL")
                self._struct.add_wall((i, j))
                tracer.log_step()
                
        # D* 의 핵심: 막힌 장애물 근처만 재탐색 알고리즘
        tracer.info("로봇 상태", "D* 발동: 충돌 주변부만 RHS 값 재계산")
        tracer.frontier((10, 11)); tracer.log_step()
        tracer.frontier((9, 11));  tracer.log_step()
        tracer.frontier((8, 12));  tracer.log_step()
        tracer.visit((9, 12));     tracer.log_step()
        
        # 재개된 경로
        tracer.info("로봇 상태", "가장 효율적인 우회로(Local) 탐색 완료. 재가동")
        route_detour = [(9, 12), (9, 13), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14)]
        for p in route_detour:
            tracer.color(p, (100, 200, 255))
            tracer.label(p, "로봇")
            tracer.log_step()
            tracer.label(p, "")
            tracer.visit(p)
            
        yield from self.replay(tracer)

if __name__ == "__main__":
    DStarDemo().run("D* 동적 로봇 경로 시각화", config_path="vizlib.json")
