"""
vizlib.hud  —  오른쪽 정보 패널
"""

from __future__ import annotations
from collections import OrderedDict
from typing import Any, Optional
import os
import pygame

_SECTION_MARKER = "__section__"

_KO_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/NanumGothic.ttf",
]


def _load_font(size: int, bold: bool = False) -> pygame.font.Font:
    for path in _KO_FONT_CANDIDATES:
        if os.path.isfile(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                continue
    return pygame.font.Font(None, size)


class HUD:
    def __init__(self, cfg: dict) -> None:
        self._cfg      = cfg
        self._entries: OrderedDict[str, Any] = OrderedDict()
        self._ready    = False
        self._f_section: Optional[pygame.font.Font] = None
        self._f_key:     Optional[pygame.font.Font] = None
        self._f_val:     Optional[pygame.font.Font] = None
        self._f_hint:    Optional[pygame.font.Font] = None

    def update(self, key: str, value: Any) -> None:
        self._entries[key] = str(value)

    def section(self, title: str) -> None:
        key = f"{_SECTION_MARKER}:{title}:{id(title)}"
        self._entries[key] = title

    def remove(self, key: str) -> None:
        self._entries.pop(key, None)

    def clear(self) -> None:
        self._entries.clear()

    def _init(self) -> None:
        if self._ready:
            return
        self._f_section = _load_font(18, bold=True)
        self._f_key     = _load_font(16)
        self._f_val     = _load_font(18, bold=True)
        self._f_hint    = _load_font(14)
        self._ready     = True

    def draw(self, surface: pygame.Surface,
             x: int, y: int, width: int, height: int) -> None:
        self._init()
        c = self._cfg["colors"]

        bg      = tuple(c["hud_bg"])
        border  = tuple(c["hud_border"])
        accent  = tuple(c["hud_accent"])
        col_key = (130, 145, 175)   # 차분한 라벨색
        col_val = (220, 228, 245)   # 밝은 값 색
        col_dim = (70,  78, 105)    # 구분선·힌트 색

        # ── 배경 ──────────────────────────────────────────
        pygame.draw.rect(surface, bg, (x, y, width, height))
        # 왼쪽 세로선 하나만 (테두리 대신)
        pygame.draw.line(surface, border, (x, y), (x, y + height), 1)

        # ── 항목 목록 ──────────────────────────────────────
        pad = 24
        cy  = y + 30

        hint_lines = [
            "R  start / restart",
            "SPACE  pause",
            "↑ ↓  speed",
            "Q  quit",
        ]
        max_y = y + height - len(hint_lines) * 20 - 40

        for raw_key, val in self._entries.items():
            if cy >= max_y:
                break

            if raw_key.startswith(_SECTION_MARKER):
                # ── 섹션 구분 ──────────────────────────────
                cy += 10
                # 점선 느낌
                pygame.draw.line(surface, col_dim,
                                 (x + pad, cy), (x + width - pad, cy), 1)
                cy += 12
                s = self._f_section.render(val.upper(), True, accent)
                surface.blit(s, (x + pad, cy))
                cy += 30
                continue

            # ── key ───────────────────────────────────────
            ks = self._f_key.render(raw_key, True, col_key)
            surface.blit(ks, (x + pad, cy))
            cy += 20

            # ── value ─────────────────────────────────────
            vs = self._f_val.render(val, True, col_val)
            surface.blit(vs, (x + pad + 10, cy))
            cy += 36

        # ── 단축키 힌트 (하단) ─────────────────────────────
        hy = y + height - len(hint_lines) * 20 - 20
        pygame.draw.line(surface, col_dim,
                         (x + pad, hy - 10), (x + width - pad, hy - 10), 1)
        for line in hint_lines:
            hs = self._f_hint.render(line, True, col_dim)
            surface.blit(hs, (x + pad, hy))
            hy += 20
