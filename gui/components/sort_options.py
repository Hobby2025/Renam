"""
Sort Options Component
정렬 옵션 UI 컴포넌트 (단일 책임: 정렬 옵션 선택 UI)
"""

from tkinter import Frame, Label, Radiobutton, Entry, Button, IntVar, StringVar
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class SortOptions(Frame):
    """
    정렬 옵션 컴포넌트
    책임: 정렬 방식 선택 UI 표시 및 선택 이벤트 처리
    """

    def __init__(self, parent, on_sort_changed: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_sort_changed: 정렬 옵션 변경 시 호출될 콜백 함수
        """
        super().__init__(parent, **ModernStyle.get_frame_style())
        self.on_sort_changed = on_sort_changed

        self.sort_mode = IntVar(value=1)  # 1: 숫자, 2: 알파벳, 3: 날짜, 4: 확장자, 5: 정규식
        self.regex_pattern = StringVar(value=r"(\d+)")

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 컨테이너
        container = Frame(self, **ModernStyle.get_frame_style())
        container.pack(fill="x", padx=ModernStyle.SPACING['xl'], pady=ModernStyle.SPACING['md'])

        # 헤더
        Label(
            container,
            text="정렬 규칙",
            font=ModernStyle.create_font('body', 'bold'),
            **ModernStyle.get_label_style('primary')
        ).pack(anchor="w", pady=(0, ModernStyle.SPACING['sm']))

        # 옵션 프레임
        options_frame = Frame(container, **ModernStyle.get_frame_style())
        options_frame.pack(fill="x", padx=ModernStyle.SPACING['md'])

        # 라디오 버튼들
        self._create_radio_option(options_frame, "숫자 기준", 1)
        self._create_radio_option(options_frame, "알파벳", 2)
        self._create_radio_option(options_frame, "생성 날짜", 3)
        self._create_radio_option(options_frame, "확장자", 4)

        # 정규식 옵션 (특별 처리)
        regex_frame = Frame(options_frame, **ModernStyle.get_frame_style())
        regex_frame.pack(anchor="w", pady=ModernStyle.SPACING['xs'])

        Radiobutton(
            regex_frame,
            text="정규식:",
            variable=self.sort_mode,
            value=5,
            command=self._on_change,
            font=ModernStyle.create_font('body'),
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_primary'],
            selectcolor=ModernStyle.COLORS['surface'],
            activebackground=ModernStyle.COLORS['surface'],
            activeforeground=ModernStyle.COLORS['accent_blue'],
            cursor="hand2"
        ).pack(side="left")

        Entry(
            regex_frame,
            textvariable=self.regex_pattern,
            font=ModernStyle.create_font('body'),
            width=20,
            **ModernStyle.get_entry_style()
        ).pack(side="left", padx=ModernStyle.SPACING['sm'])

        Button(
            regex_frame,
            text="적용",
            font=ModernStyle.create_font('caption'),
            command=self._on_change,
            cursor="hand2",
            **ModernStyle.get_button_style('secondary')
        ).pack(side="left")

        # 하단 구분선
        Frame(self, height=1, bg=ModernStyle.COLORS['separator']).pack(fill="x", pady=ModernStyle.SPACING['md'])

    def _create_radio_option(self, parent, text: str, value: int):
        """
        라디오 버튼 옵션 생성

        Args:
            parent: 부모 위젯
            text: 표시 텍스트
            value: 값
        """
        Radiobutton(
            parent,
            text=text,
            variable=self.sort_mode,
            value=value,
            command=self._on_change,
            font=ModernStyle.create_font('body'),
            bg=ModernStyle.COLORS['surface'],
            fg=ModernStyle.COLORS['text_primary'],
            selectcolor=ModernStyle.COLORS['surface'],
            activebackground=ModernStyle.COLORS['surface'],
            activeforeground=ModernStyle.COLORS['accent_blue'],
            cursor="hand2"
        ).pack(anchor="w", pady=ModernStyle.SPACING['xs'])

    def _on_change(self):
        """정렬 옵션 변경 이벤트"""
        if self.on_sort_changed:
            self.on_sort_changed()

    def get_sort_mode(self) -> int:
        """
        현재 선택된 정렬 모드 반환

        Returns:
            정렬 모드 (1~5)
        """
        return self.sort_mode.get()

    def get_regex_pattern(self) -> str:
        """
        정규식 패턴 반환

        Returns:
            정규식 패턴 문자열
        """
        return self.regex_pattern.get()

    def set_sort_mode(self, mode: int):
        """
        정렬 모드 설정

        Args:
            mode: 정렬 모드 (1~5)
        """
        self.sort_mode.set(mode)
