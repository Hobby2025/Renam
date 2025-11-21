"""
Sort Options Component
정렬 옵션 UI 컴포넌트 (단일 책임: 정렬 옵션 선택 UI)
"""

import customtkinter as ctk
from tkinter import IntVar, StringVar
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class SortOptions(ctk.CTkFrame):
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
        super().__init__(parent, fg_color="transparent")
        self.on_sort_changed = on_sort_changed

        self.sort_mode = IntVar(value=1)  # 1: 숫자, 2: 알파벳, 3: 날짜, 4: 확장자
        self.regex_pattern = StringVar(value=r"(\d+)")

        self._create_ui()

    def _create_ui(self):
        """UI 생성 (웹 스타일 카드)"""
        # 카드 스타일 컨테이너
        card = ctk.CTkFrame(
            self,
            **ModernStyle.get_card_style()
        )
        card.pack(fill="x", padx=ModernStyle.SPACING['xs'], pady=ModernStyle.SPACING['xs'])

        # 내부 패딩을 위한 컨테이너
        inner_container = ctk.CTkFrame(card, fg_color="transparent")
        inner_container.pack(fill="x", padx=ModernStyle.SPACING['lg'],
                            pady=ModernStyle.SPACING['md'])

        # 헤더
        header_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, ModernStyle.SPACING['md']))

        ctk.CTkLabel(
            header_frame,
            text="정렬 규칙",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 옵션 프레임
        options_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        options_frame.pack(fill="x")

        # 라디오 버튼들 (2열 그리드)
        self._create_radio_option(options_frame, "숫자", 1, 0, 0)
        self._create_radio_option(options_frame, "알파벳", 2, 0, 1)
        self._create_radio_option(options_frame, "날짜", 3, 1, 0)
        self._create_radio_option(options_frame, "확장자", 4, 1, 1)

    def _create_radio_option(self, parent, text: str, value: int, row: int, col: int):
        """
        라디오 버튼 옵션 생성
        """
        ctk.CTkRadioButton(
            parent,
            text=text,
            variable=self.sort_mode,
            value=value,
            command=self._on_change,
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_primary'],
            fg_color=ModernStyle.COLORS['accent_blue'],
            hover_color=ModernStyle.COLORS['accent_blue_dark']
        ).grid(row=row, column=col, sticky="w", padx=ModernStyle.SPACING['sm'], pady=ModernStyle.SPACING['xs'])

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
