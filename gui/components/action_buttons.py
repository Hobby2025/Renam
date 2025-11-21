"""
Action Buttons Component
액션 버튼 UI 컴포넌트 (단일 책임: 액션 버튼 UI)
"""

import customtkinter as ctk
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class ActionButtons(ctk.CTkFrame):
    """
    액션 버튼 컴포넌트
    책임: 실행, 되돌리기, 종료 버튼 표시 및 이벤트 처리
    """

    def __init__(self, parent,
                 on_execute: Optional[Callable] = None,
                 on_undo: Optional[Callable] = None,
                 on_quit: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_execute: 실행 버튼 클릭 시 호출될 콜백
            on_undo: 되돌리기 버튼 클릭 시 호출될 콜백
            on_quit: 종료 버튼 클릭 시 호출될 콜백
        """
        super().__init__(parent, fg_color="transparent")
        self.on_execute = on_execute
        self.on_undo = on_undo
        self.on_quit = on_quit

        self.undo_button = None  # 되돌리기 버튼 참조

        self._create_ui()

    def _create_ui(self):
        """UI 생성 (웹 스타일)"""
        # 카드 스타일 컨테이너
        card = ctk.CTkFrame(
            self,
            **ModernStyle.get_card_style()
        )
        card.pack(fill="x", padx=ModernStyle.SPACING['xs'], pady=ModernStyle.SPACING['xs'])

        # 내부 패딩을 위한 컨테이너
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=ModernStyle.SPACING['lg'],
                      pady=ModernStyle.SPACING['md'])

        # 좌측: 변경 버튼 (더 크고 눈에 띄게)
        ctk.CTkButton(
            container,
            text="변경",
            font=ModernStyle.create_font('body', 'bold'),
            width=120,
            height=36,
            command=lambda: self.on_execute() if self.on_execute else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_success'],
            text_color=ModernStyle.COLORS['text_button'],
            hover_color=ModernStyle.COLORS['button_success_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        # 되돌리기 버튼 (초기에는 비활성화)
        self.undo_button = ctk.CTkButton(
            container,
            text="되돌리기",
            font=ModernStyle.create_font('body', 'bold'),
            width=120,
            height=36,
            command=self._undo_click_handler,
            fg_color=ModernStyle.COLORS['button_secondary'],  # 초기 비활성화 색상
            text_color=ModernStyle.COLORS['text_disabled'],
            hover_color=ModernStyle.COLORS['button_secondary'],
            corner_radius=ModernStyle.RADIUS['sm'],
            state="disabled"
        )
        self.undo_button.pack(side="left", padx=ModernStyle.SPACING['sm'])

        self.undo_enabled = False  # 상태 추적 변수

        # 우측: 종료 버튼
        ctk.CTkButton(
            container,
            text="종료",
            font=ModernStyle.create_font('body', 'bold'),
            width=120,
            height=36,
            command=lambda: self.on_quit() if self.on_quit else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_danger'],
            text_color=ModernStyle.COLORS['text_button'],
            hover_color=ModernStyle.COLORS['button_danger_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="right")

    def _undo_click_handler(self):
        """되돌리기 버튼 클릭 핸들러"""
        if self.undo_enabled and self.on_undo:
            self.on_undo()

    def enable_undo(self):
        """되돌리기 버튼 활성화"""
        if self.undo_button:
            self.undo_enabled = True
            self.undo_button.configure(
                state="normal",
                fg_color=ModernStyle.COLORS['button_warning'],
                text_color=ModernStyle.COLORS['text_button'],
                hover_color=ModernStyle.COLORS['button_warning_hover']
            )

    def disable_undo(self):
        """되돌리기 버튼 비활성화"""
        if self.undo_button:
            self.undo_enabled = False
            self.undo_button.configure(
                state="disabled",
                fg_color=ModernStyle.COLORS['button_secondary'],
                text_color=ModernStyle.COLORS['text_disabled'],
                hover_color=ModernStyle.COLORS['button_secondary']
            )
