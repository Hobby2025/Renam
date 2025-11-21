"""
Tab Manager Component
탭 관리 UI 컴포넌트 (단일 책임: 하위 폴더 탭 관리)
"""

import customtkinter as ctk
from pathlib import Path
from typing import Optional, Callable, List
from gui.modern_style import ModernStyle


class TabManager(ctk.CTkFrame):
    """
    탭 관리 컴포넌트
    책임: 하위 폴더를 탭으로 표시하고 선택 관리
    """

    def __init__(self, parent, on_tab_changed: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_tab_changed: 탭 변경 시 호출될 콜백 (folder_name: str)
        """
        super().__init__(parent, fg_color="transparent")
        self.on_tab_changed = on_tab_changed

        self.tabs: List[str] = []  # 탭 이름 리스트 (폴더명)
        self.current_tab: Optional[str] = None  # 현재 선택된 탭
        self.tab_buttons: dict = {}  # 탭 버튼 위젯 저장

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 카드 스타일 컨테이너
        card = ctk.CTkFrame(
            self,
            **ModernStyle.get_card_style()
        )
        card.pack(fill="x", padx=ModernStyle.SPACING['xs'], pady=ModernStyle.SPACING['xs'])

        # 내부 패딩
        self.inner_container = ctk.CTkFrame(card, fg_color="transparent")
        self.inner_container.pack(fill="x", padx=ModernStyle.SPACING['lg'],
                                  pady=ModernStyle.SPACING['md'])

        # 헤더
        header_frame = ctk.CTkFrame(self.inner_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, ModernStyle.SPACING['md']))

        ctk.CTkLabel(
            header_frame,
            text="📁",
            font=ModernStyle.create_font('headline'),
            text_color=ModernStyle.COLORS['text_tertiary']
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        ctk.CTkLabel(
            header_frame,
            text="하위 폴더",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 탭 버튼 컨테이너
        self.tabs_container = ctk.CTkScrollableFrame(
            self.inner_container,
            fg_color="transparent",
            height=180,
            orientation="horizontal"
        )
        self.tabs_container.pack(fill="x")

        # 초기 메시지
        self.empty_label = ctk.CTkLabel(
            self.tabs_container,
            text="폴더를 선택하면 하위 폴더가 탭으로 표시됩니다.",
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.empty_label.pack(pady=ModernStyle.SPACING['sm'])

    def set_tabs(self, folder_names: List[str]):
        """
        탭 설정

        Args:
            folder_names: 하위 폴더명 리스트
        """
        # 기존 탭 제거
        for widget in self.tabs_container.winfo_children():
            widget.destroy()

        self.tabs = folder_names
        self.tab_buttons = {}
        self.current_tab = None

        if not folder_names:
            self.empty_label = ctk.CTkLabel(
                self.tabs_container,
                text="하위 폴더가 없습니다.",
                font=ModernStyle.create_font('caption'),
                text_color=ModernStyle.COLORS['text_tertiary']
            )
            self.empty_label.pack(pady=ModernStyle.SPACING['sm'])
            return

        # "전체" 탭 추가
        self._create_tab_button("전체", is_all_tab=True)

        # 각 폴더를 탭으로 생성
        for folder_name in folder_names:
            self._create_tab_button(folder_name)

        # 첫 번째 탭 선택
        if folder_names:
            self.select_tab(folder_names[0])

    def _create_tab_button(self, name: str, is_all_tab: bool = False):
        """
        탭 버튼 생성

        Args:
            name: 탭 이름
            is_all_tab: 전체 탭 여부
        """
        btn = ctk.CTkButton(
            self.tabs_container,
            text=name,
            font=ModernStyle.create_font('micro'),
            height=8,  # Reduced height for a more compact tab button
            corner_radius=ModernStyle.RADIUS['xs'],
            fg_color=ModernStyle.COLORS['button_secondary'],
            text_color=ModernStyle.COLORS['text_primary'],
            hover_color=ModernStyle.COLORS['button_secondary_hover'],
            command=lambda: self.select_tab(name)
        )
        btn.pack(side="left", padx=ModernStyle.SPACING['xs'])

        self.tab_buttons[name] = btn

    def select_tab(self, tab_name: str):
        """
        탭 선택

        Args:
            tab_name: 선택할 탭 이름
        """
        if tab_name not in self.tab_buttons:
            return

        self.current_tab = tab_name

        # 모든 탭 비활성화 스타일
        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                # 선택된 탭
                btn.configure(
                    fg_color=ModernStyle.COLORS['accent_blue'],
                    text_color=ModernStyle.COLORS['text_button'],
                    hover_color=ModernStyle.COLORS['accent_blue_dark']
                )
            else:
                # 비선택 탭
                btn.configure(
                    fg_color=ModernStyle.COLORS['button_secondary'],
                    text_color=ModernStyle.COLORS['text_primary'],
                    hover_color=ModernStyle.COLORS['button_secondary_hover']
                )

        # 콜백 호출
        if self.on_tab_changed:
            self.on_tab_changed(tab_name)

    def get_current_tab(self) -> Optional[str]:
        """현재 선택된 탭 반환"""
        return self.current_tab

    def clear(self):
        """탭 초기화"""
        self.set_tabs([])
