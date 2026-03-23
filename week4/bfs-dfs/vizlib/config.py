"""
vizlib.config
─────────────────────────────────────────────────────
설정 기본값 정의 및 JSON 파일 로드.

타일 크기 자동 계산
--------------------
tile_size = 0 (기본값) 이면 엔진이 target_grid_w / target_grid_h 를 기준으로
그리드 행·열 수에 맞게 타일 크기를 역산한다.

    target_grid_w / target_grid_h  : 그리드 영역 목표 픽셀 크기
    max_tile_size / min_tile_size  : 자동 계산 결과의 상한 · 하한

tile_size > 0 으로 명시하면 자동 계산을 건너뛰고 해당 값을 그대로 사용한다.

tile_shape 자동 결정
---------------------
Scene 이 use(struct) 로 자료구조를 등록할 때,
NodeGraph / TreeNode 이면 engine._tile_shape = "circle" 로 설정한다.
나머지(Grid2D, Array1D, ...)는 "rect" (둥근 사각형).

Circle → border_radius = tile_size // 2
Rect   → border_radius = max(2, tile_size // 6)
"""

import json
import os
from copy import deepcopy
from typing import Optional, Tuple

# ── 기본 설정 ─────────────────────────────────────────────────────
DEFAULTS: dict = {
    "title":            "vizlib",

    # 그리드 크기 (Scene 사용 시 자료구조에서 자동 덮어씀)
    "grid_rows":        20,
    "grid_cols":        20,

    # 타일 크기 — 0 이면 target_grid_w/h 에서 자동 계산
    "tile_size":        0,
    "tile_margin":      2,

    # 자동 계산 목표 창 크기 및 타일 크기 범위
    "target_grid_w":    700,
    "target_grid_h":    600,
    "max_tile_size":    64,
    "min_tile_size":    6,

    "fps":              60,
    "step_interval_ms": 60,
    "hud_width":        220,

    "colors": {
        "background":   [10,  10,  15],  # Deep OLED Black
        "unvisited":    [20,  22,  30],  # Soft Dark Grey
        "frontier":     [255, 140, 0],   # Neon Orange
        "visited":      [20,  60,  130], # Deep Neon Blue
        "wall":         [40,  42,  50],  
        "start":        [10,  250, 150], # Neon Mint Green
        "end":          [255, 50,  80],  # Neon Red
        "path":         [0,   255, 255], # Neon Cyan (형광 하늘색)
        "text_tile":    [255, 255, 255], 
        "text_hud":     [220, 225, 235],
        "hud_bg":       [15,  15,  20],
        "hud_border":   [40,  45,  60],
        "hud_accent":   [0,   255, 255],
        "hint_text":    [80,  85,  105],
    },
}


def _deep_update(base: dict, override: dict) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v


def load_config(path: Optional[str] = None) -> dict:
    """기본값에 JSON 파일을 덮어씌운 설정 dict 를 반환한다."""
    cfg = deepcopy(DEFAULTS)
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            _deep_update(cfg, json.load(f))
    return cfg


def color(cfg: dict, name: str) -> Tuple[int, int, int]:
    """설정에서 색상 이름으로 RGB 튜플을 꺼낸다."""
    return tuple(cfg["colors"].get(name, cfg["colors"]["unvisited"]))
