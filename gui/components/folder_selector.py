"""
Folder Selector Component
폴더 선택 UI 컴포넌트 (단일 책임: 폴더 선택 UI)
"""

import customtkinter as ctk
from tkinter import filedialog, StringVar
from pathlib import Path
from typing import Optional, Callable
import os
from gui.modern_style import ModernStyle


class FolderSelector(ctk.CTkFrame):
    """
    폴더 선택 컴포넌트
    책임: 폴더 선택 UI 표시 및 폴더 선택 이벤트 처리
    """

    def __init__(self, parent, on_folder_selected: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_folder_selected: 폴더 선택 시 호출될 콜백 함수
        """
        super().__init__(parent, fg_color="transparent")
        self.on_folder_selected = on_folder_selected

        self.folder_var = StringVar(value="폴더를 선택하세요")
        self.selected_folder: Optional[Path] = None

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

        # 좌측: 아이콘 + 레이블
        left_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)

        header_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        header_frame.pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="📂",
            font=ModernStyle.create_font('headline'),
            text_color=ModernStyle.COLORS['text_primary'],
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        ctk.CTkLabel(
            header_frame,
            text="폴더 선택",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 우측: 찾아보기 버튼
        browse_btn = ctk.CTkButton(
            inner_container,
            text="찾아보기",
            font=ModernStyle.create_font('body'),
            command=self._on_browse,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_primary'],
            text_color=ModernStyle.COLORS['text_button'],
            hover_color=ModernStyle.COLORS['button_primary_hover'],
            corner_radius=ModernStyle.RADIUS['sm'],
            height=36
        )
        browse_btn.pack(side="right", padx=(ModernStyle.SPACING['md'], 0))

        # 중앙: 브레드크럼 (일반 프레임으로 변경하여 스크롤바 제거)
        self.breadcrumb_frame = ctk.CTkFrame(
            inner_container,
            height=36,
            fg_color="transparent"
        )
        self.breadcrumb_frame.pack(side="left", fill="x", expand=True, padx=(ModernStyle.SPACING['md'], 0))
        
        # 초기 텍스트
        self.placeholder_label = ctk.CTkLabel(
            self.breadcrumb_frame,
            text="폴더를 선택해주세요",
            font=ModernStyle.create_font('body'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.placeholder_label.pack(side="left", pady=0)

    def _update_breadcrumb(self, path: Path):
        """브레드크럼 업데이트"""
        # 기존 위젯 제거
        for widget in self.breadcrumb_frame.winfo_children():
            widget.destroy()

        parts = list(path.parts)
        style = ModernStyle.get_breadcrumb_style()
        
        # 경로가 너무 길면 앞부분 생략 (...)
        # 최대 표시 개수 제한 (예: 4개)
        if len(parts) > 4:
            parts = [parts[0], "..."] + parts[-3:]
            
        for i, part in enumerate(parts):
            # 구분자
            if i > 0:
                ctk.CTkLabel(
                    self.breadcrumb_frame,
                    text="›",
                    font=ModernStyle.create_font('body', 'bold'),
                    text_color=style['text_color']
                ).pack(side="left", padx=2, pady=0)

            # 폴더명 (마지막 요소 강조)
            is_last = (i == len(parts) - 1)
            
            # 칩 스타일
            fg_color = style['bg_color'] if not is_last else ModernStyle.COLORS['accent_blue']
            text_color = style['text_color_active'] if not is_last else '#FFFFFF'
            hover_color = style['hover_color'] if not is_last else ModernStyle.COLORS['accent_blue_dark']
            
            # 드라이브 문자 뒤 슬래시 제거 및 ... 처리
            display_text = part
            if part != "..." and part.endswith(os.sep):
                display_text = part.rstrip(os.sep)
                
            btn = ctk.CTkButton(
                self.breadcrumb_frame,
                text=display_text,
                font=ModernStyle.create_font('caption', 'bold' if is_last else 'normal'),
                text_color=text_color,
                fg_color=fg_color,
                hover_color=hover_color,
                width=0,
                height=28,
                corner_radius=14,
                command=lambda: None 
            )
            btn.pack(side="left", padx=2, pady=4)

    def _on_browse(self):
        """폴더 찾아보기 버튼 클릭 이벤트"""
        folder_selected = filedialog.askdirectory(title="이미지 폴더를 선택하세요")
        if folder_selected:
            path = Path(folder_selected)
            self.selected_folder = path
            self.folder_var.set(str(path))
            self._update_breadcrumb(path)  # 브레드크럼 업데이트
            
            if self.on_folder_selected:
                self.on_folder_selected(path)

    def get_selected_folder(self) -> Optional[Path]:
        """
        선택된 폴더 반환

        Returns:
            선택된 폴더 경로 또는 None
        """
        return self.selected_folder

    def reset(self):
        """폴더 선택 초기화"""
        self.selected_folder = None
        self.folder_var.set("폴더를 선택하세요")
        
        # 브레드크럼 초기화
        for widget in self.breadcrumb_frame.winfo_children():
            widget.destroy()
            
        self.placeholder_label = ctk.CTkLabel(
            self.breadcrumb_frame,
            text="폴더를 선택해주세요",
            font=ModernStyle.create_font('body'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.placeholder_label.pack(side="left", pady=5)
