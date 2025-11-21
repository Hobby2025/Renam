"""
Pattern Input Component
파일명 패턴 입력 UI 컴포넌트 (단일 책임: 패턴 입력 UI)
"""

import customtkinter as ctk
from tkinter import StringVar
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class PatternInput(ctk.CTkFrame):
    """
    파일명 패턴 입력 컴포넌트
    책임: 파일명 패턴 입력 UI 표시 (Combobox + Entry)
    """

    def __init__(self, parent, on_pattern_changed: Optional[Callable] = None):
        super().__init__(parent, fg_color="transparent")
        
        self.on_pattern_changed = on_pattern_changed
        self.mode_var = StringVar(value="숫자")
        self.prefix_var = StringVar(value="")
        
        # 변경 감지를 위한 trace 추가
        self.mode_var.trace_add("write", lambda *args: self._notify_change())
        self.prefix_var.trace_add("write", lambda *args: self._notify_change())
        
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
            text="파일명 패턴",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 입력 프레임
        input_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        input_frame.pack(fill="x")

        # 1. 패턴 선택 (라디오 버튼으로 변경)
        pattern_options_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        pattern_options_frame.pack(fill="x", pady=(0, ModernStyle.SPACING['xs']))
        
        # 첫 번째 행 (숫자, 알파벳)
        row1 = ctk.CTkFrame(pattern_options_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, ModernStyle.SPACING['xs']))
        
        ctk.CTkRadioButton(
            row1,
            text="숫자",
            variable=self.mode_var,
            value="숫자",
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_primary'],
            fg_color=ModernStyle.COLORS['accent_blue'],
            border_color=ModernStyle.COLORS['border'],
            hover_color=ModernStyle.COLORS['surface_hover'],
            command=self._on_mode_change
        ).pack(side="left", padx=(0, ModernStyle.SPACING['xl']))
        
        ctk.CTkRadioButton(
            row1,
            text="파일명_숫자",
            variable=self.mode_var,
            value="파일명_숫자",
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_primary'],
            fg_color=ModernStyle.COLORS['accent_blue'],
            border_color=ModernStyle.COLORS['border'],
            hover_color=ModernStyle.COLORS['surface_hover'],
            command=self._on_mode_change
        ).pack(side="left")

        # 2. 파일명 입력 (Entry)
        self.entry_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        self.entry_frame.pack(fill="x", pady=(ModernStyle.SPACING['sm'], 0))

        ctk.CTkLabel(
            self.entry_frame,
            text="파일명:",
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_secondary']
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        self.prefix_entry = ctk.CTkEntry(
            self.entry_frame,
            textvariable=self.prefix_var,
            font=ModernStyle.create_font('body'),
            width=180,
            corner_radius=ModernStyle.RADIUS['sm'],
            border_color=ModernStyle.COLORS['border'],
            fg_color=ModernStyle.COLORS['surface'],
            text_color=ModernStyle.COLORS['text_primary']
        )
        self.prefix_entry.pack(side="left")

        # 초기 상태 설정
        self._on_mode_change()

    def _on_mode_change(self, choice=None):
        """모드 변경 시 이벤트"""
        mode = self.mode_var.get()
        if mode == "숫자":
            self.prefix_entry.configure(state="disabled")
        else:
            self.prefix_entry.configure(state="normal")
    
    def _notify_change(self):
        """패턴 변경 알림"""
        if self.on_pattern_changed:
            self.on_pattern_changed()

    def get_pattern(self) -> str:
        """
        현재 설정된 패턴 반환
        """
        mode = self.mode_var.get()
        if mode == "숫자":
            return "{n}"
        elif mode == "파일명_숫자":
            prefix = self.prefix_var.get()
            return f"{prefix}_{{n}}"
        return "{n}"

    def set_pattern(self, pattern: str):
        """
        패턴 설정

        Args:
            pattern: 설정할 패턴 문자열 (예: "{n}", "image_{n}")
        """
        if pattern == "{n}":
            self.mode_var.set("숫자")
            self.prefix_var.set("")
        elif "_" in pattern and "{n}" in pattern:
            # "prefix_{n}" 형식
            prefix = pattern.split("_{n}")[0]
            self.mode_var.set("파일명_숫자")
            self.prefix_var.set(prefix)
        else:
            # 기본값
            self.mode_var.set("숫자")
            self.prefix_var.set("")
