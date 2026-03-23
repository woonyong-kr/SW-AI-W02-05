"""
vizlib.tracer
─────────────────────────────────────────────────────
순수 알고리즘 코드 안에서 시각화 엔진 동작을 지시하는 객체.
알고리즘 내부를 더럽히지(Color, Shape 등) 않고 이벤트만 던집니다.
"""

class Tracer:
    def __init__(self):
        self.events = []

    def log_step(self):
        """한 단계(프레임) 진행 (yield 대체)"""
        self.events.append(("step",))

    def visit(self, node):
        self.events.append(("visit", node))

    def frontier(self, node):
        self.events.append(("frontier", node))

    def path(self, node):
        self.events.append(("path", node))

    def label(self, node, text):
        self.events.append(("label", node, text))

    def color(self, node, rgb):
        self.events.append(("color", node, rgb))

    def info(self, key, value):
        self.events.append(("info", key, value))

    def unvisit(self, node):
        self.events.append(("unvisit", node))

    def start(self, node):
        self.events.append(("start", node))

    def end(self, node):
        self.events.append(("end", node))
