"""
Pattern Input Component
파일명 패턴 입력 UI 컴포넌트 (단일 책임: 패턴 입력 UI)
"""

from tkinter import Frame, Label, Entry, StringVar
from gui.modern_style import ModernStyle
from core.name_generator import NameGenerator


class PatternInput(Frame):
    """
    파일명 패턴 입력 컴포넌트
    책임: 파일명 패턴 입력 UI 표시
    """

    def __init__(self, parent):
        """
        초기화

        Args:
            parent: 부모 위젯
        """
        super().__init__(parent, **ModernStyle.get_frame_style())

        self.pattern_var = StringVar(value="{n}")

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 컨테이너
        container = Frame(self, **ModernStyle.get_frame_style())
        container.pack(fill="x", padx=ModernStyle.SPACING['xl'], pady=ModernStyle.SPACING['md'])

        # 헤더
        Label(
            container,
            text="파일명 패턴",
            font=ModernStyle.create_font('body', 'bold'),
            **ModernStyle.get_label_style('primary')
        ).pack(anchor="w", pady=(0, ModernStyle.SPACING['sm']))

        # 입력 필드 프레임
        input_frame = Frame(container, **ModernStyle.get_frame_style())
        input_frame.pack(fill="x", padx=ModernStyle.SPACING['md'])

        # 입력 필드
        entry = Entry(
            input_frame,
            textvariable=self.pattern_var,
            font=ModernStyle.create_font('body'),
            width=30,
            **ModernStyle.get_entry_style()
        )
        entry.pack(anchor="w", pady=ModernStyle.SPACING['xs'])

        # 예시 텍스트
        example_text = NameGenerator.get_pattern_examples()
        Label(
            input_frame,
            text=example_text,
            font=ModernStyle.create_font('caption'),
            **ModernStyle.get_label_style('tertiary')
        ).pack(anchor="w", pady=(ModernStyle.SPACING['xs'], 0))

        # 하단 구분선
        Frame(self, height=1, bg=ModernStyle.COLORS['separator']).pack(fill="x", pady=ModernStyle.SPACING['md'])

    def get_pattern(self) -> str:
        """
        현재 입력된 패턴 반환

        Returns:
            파일명 패턴 문자열
        """
        return self.pattern_var.get()

    def set_pattern(self, pattern: str):
        """
        패턴 설정

        Args:
            pattern: 파일명 패턴
        """
        self.pattern_var.set(pattern)
