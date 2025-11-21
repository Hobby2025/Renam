"""
Preview Table Component
미리보기 테이블 UI 컴포넌트 (단일 책임: 파일 목록 미리보기 UI)
"""

import customtkinter as ctk
from tkinter import Listbox, Scrollbar
from typing import List, Optional, Callable
from gui.modern_style import ModernStyle
from models.file_item import FileItem


class PreviewTable(ctk.CTkFrame):
    """
    미리보기 테이블 컴포넌트
    책임: 파일 목록 표시 및 순서 변경 UI
    """

    def __init__(self, parent, on_move_up: Optional[Callable] = None,
                 on_move_down: Optional[Callable] = None,
                 on_remove: Optional[Callable] = None,
                 on_reset: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_move_up: 위로 이동 버튼 클릭 시 호출될 콜백
            on_move_down: 아래로 이동 버튼 클릭 시 호출될 콜백
            on_remove: 제거 버튼 클릭 시 호출될 콜백
            on_reset: 초기화 버튼 클릭 시 호출될 콜백
        """
        super().__init__(parent, fg_color="transparent")
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down
        self.on_remove = on_remove
        self.on_reset = on_reset

        self.file_listbox: Optional[Listbox] = None
        
        # 다중 선택을 위한 변수
        self.selected_indices = set()  # 선택된 인덱스들
        self.last_selected_index = None  # 마지막 선택된 인덱스 (Shift 선택용)
        self.row_widgets = [] # 위젯 리스트 초기화

        self._create_ui()

    def _create_ui(self):
        """UI 생성 (웹 스타일 카드)"""
        # 카드 스타일 컨테이너
        card = ctk.CTkFrame(
            self,
            **ModernStyle.get_card_style()
        )
        card.pack(fill="both", expand=True, padx=ModernStyle.SPACING['xs'],
                 pady=ModernStyle.SPACING['xs'])

        # 내부 패딩을 위한 컨테이너
        inner_container = ctk.CTkFrame(card, fg_color="transparent")
        inner_container.pack(fill="both", expand=True, padx=ModernStyle.SPACING['lg'],
                            pady=ModernStyle.SPACING['md'])

        # 헤더
        header_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, ModernStyle.SPACING['md']))

        ctk.CTkLabel(
            header_frame,
            text="미리보기",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 테이블 프레임
        table_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        # 테이블 헤더 (Grid 사용)
        header_grid = ctk.CTkFrame(
            table_frame,
            fg_color=ModernStyle.COLORS['background_secondary'],
            corner_radius=0,
            height=40
        )
        header_grid.pack(fill="x", padx=1, pady=(1, 0))
        
        # Grid 설정 (비율 조정)
        header_grid.grid_columnconfigure(0, weight=8)  # 원본 파일명
        header_grid.grid_columnconfigure(1, weight=1)  # 화살표
        header_grid.grid_columnconfigure(2, weight=1)  # 변경 파일명

        ctk.CTkLabel(
            header_grid,
            text="원본 파일명",
            font=ModernStyle.create_font('caption', 'bold'),
            text_color=ModernStyle.COLORS['text_default'],
            anchor="w"  # 왼쪽 정렬
        ).grid(row=0, column=0, sticky="ew", padx=ModernStyle.SPACING['lg'], pady=ModernStyle.SPACING['sm'])

        ctk.CTkLabel(
            header_grid,
            text="→",  # 화살표 추가
            font=ModernStyle.create_font('caption', 'bold'),
            text_color=ModernStyle.COLORS['text_tertiary'],
            width=40
        ).grid(row=0, column=1)

        ctk.CTkLabel(
            header_grid,
            text="변경 파일명",
            font=ModernStyle.create_font('caption', 'bold'),
            text_color=ModernStyle.COLORS['text_default'],
            anchor="w"  # 왼쪽 정렬
        ).grid(row=0, column=2, sticky="ew", padx=ModernStyle.SPACING['lg'], pady=ModernStyle.SPACING['sm'])

        # 파일 목록 (ScrollableFrame + Grid)
        self.list_frame = ctk.CTkScrollableFrame(
            table_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.list_frame.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        # Grid 설정 (헤더와 동일하게)
        self.list_frame.grid_columnconfigure(0, weight=8)
        self.list_frame.grid_columnconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(2, weight=4)

        # 빈 상태 메시지
        self.empty_label = ctk.CTkLabel(
            self.list_frame,
            text="표시할 파일이 없습니다.",
            font=ModernStyle.create_font('body'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.empty_label.pack(pady=ModernStyle.SPACING['xl'])

        # 하단: 버튼들 (가로 배치)
        button_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(ModernStyle.SPACING['md'], 0))

        # 버튼들을 중앙에 배치
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(anchor="center")

        # 위로 버튼
        ctk.CTkButton(
            button_container,
            text="↑ 위로",
            width=110,
            height=36,
            font=ModernStyle.create_font('body'),
            command=lambda: self.on_move_up() if self.on_move_up else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_secondary'],
            text_color=ModernStyle.COLORS['text_primary'],
            hover_color=ModernStyle.COLORS['button_secondary_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="left", padx=ModernStyle.SPACING['xs'])

        # 아래로 버튼
        ctk.CTkButton(
            button_container,
            text="↓ 아래로",
            width=110,
            height=36,
            font=ModernStyle.create_font('body'),
            command=lambda: self.on_move_down() if self.on_move_down else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_secondary'],
            text_color=ModernStyle.COLORS['text_primary'],
            hover_color=ModernStyle.COLORS['button_secondary_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="left", padx=ModernStyle.SPACING['xs'])

        # 제거 버튼
        ctk.CTkButton(
            button_container,
            text="제거",
            width=110,
            height=36,
            font=ModernStyle.create_font('body'),
            command=lambda: self.on_remove() if self.on_remove else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_danger'],
            text_color=ModernStyle.COLORS['text_button'],
            hover_color=ModernStyle.COLORS['button_danger_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="left", padx=ModernStyle.SPACING['xs'])

        # 초기화 버튼 (추가됨)
        ctk.CTkButton(
            button_container,
            text="초기화",
            width=110,
            height=36,
            font=ModernStyle.create_font('body'),
            command=lambda: self.on_reset() if self.on_reset else None,
            cursor="hand2",
            fg_color=ModernStyle.COLORS['button_primary'],
            text_color=ModernStyle.COLORS['text_button'],
            hover_color=ModernStyle.COLORS['button_primary_hover'],
            corner_radius=ModernStyle.RADIUS['sm']
        ).pack(side="left", padx=ModernStyle.SPACING['xs'])

    def update_preview(self, file_items: List[FileItem]):
        """
        미리보기 테이블 업데이트 (최적화: 위젯 재사용)
        """
        if not file_items:
            # 모든 위젯 숨기기
            for row in self.row_widgets:
                for widget in [row['orig'], row['arrow'], row['new']]:
                    widget.grid_remove()
            
            if not hasattr(self, 'empty_label') or not self.empty_label.winfo_exists():
                self.empty_label = ctk.CTkLabel(
                    self.list_frame,
                    text="표시할 파일이 없습니다.",
                    font=ModernStyle.create_font('body'),
                    text_color=ModernStyle.COLORS['text_tertiary']
                )
                self.empty_label.pack(pady=ModernStyle.SPACING['xl'])
            else:
                self.empty_label.pack(pady=ModernStyle.SPACING['xl'])
            
            self.selected_indices.clear()
            return

        # 빈 상태 라벨 제거
        if hasattr(self, 'empty_label') and self.empty_label.winfo_exists():
            self.empty_label.pack_forget()

        style = ModernStyle.get_table_style()
        current_count = len(self.row_widgets)
        target_count = len(file_items)

        # 1. 부족한 위젯 추가
        for i in range(current_count, target_count):
            # 원본 파일명
            lbl_orig = ctk.CTkLabel(
                self.list_frame,
                text="",
                font=ModernStyle.create_font('body'),
                text_color=ModernStyle.COLORS['text_primary'],
                anchor="w",
                corner_radius=4
            )
            
            # 화살표
            lbl_arrow = ctk.CTkLabel(
                self.list_frame,
                text="→",
                font=ModernStyle.create_font('body'),
                text_color=ModernStyle.COLORS['text_tertiary'],
                anchor="center"
            )
            
            # 변경 파일명
            lbl_new = ctk.CTkLabel(
                self.list_frame,
                text="",
                font=ModernStyle.create_font('body'),
                text_color=ModernStyle.COLORS['text_primary'],
                anchor="w",
                corner_radius=4
            )
            
            # 이벤트 바인딩
            for widget in [lbl_orig, lbl_arrow, lbl_new]:
                widget.bind("<Button-1>", lambda e, idx=i: self._on_row_click(e, idx))
            
            self.row_widgets.append({
                'orig': lbl_orig,
                'arrow': lbl_arrow,
                'new': lbl_new,
                'bg': ''  # 나중에 설정됨
            })

        # 2. 위젯 업데이트 및 배치
        for i, item in enumerate(file_items):
            row = self.row_widgets[i]
            
            # 배경색 결정
            is_selected = i in self.selected_indices
            base_bg = style['row_bg'] if i % 2 == 0 else style['row_bg_alt']
            bg_color = style['row_selected'] if is_selected else base_bg
            row['bg'] = base_bg  # 기본 배경색 저장

            # 원본 파일명 업데이트
            row['orig'].configure(text=item.original_name, fg_color=bg_color)
            row['orig'].grid(row=i, column=0, sticky="ew", padx=ModernStyle.SPACING['lg'], pady=1, ipady=5)
            
            # 화살표 업데이트
            row['arrow'].configure(fg_color=bg_color)
            row['arrow'].grid(row=i, column=1, sticky="ew", padx=0, pady=1, ipady=5)
            
            # 변경 파일명 업데이트
            is_changed = item.original_name != item.new_name
            text_color = ModernStyle.COLORS['accent_blue'] if is_changed else ModernStyle.COLORS['text_primary']
            weight = 'bold' if is_changed else 'normal'
            
            row['new'].configure(
                text=item.new_name, 
                text_color=text_color, 
                font=ModernStyle.create_font('body', weight),
                fg_color=bg_color
            )
            row['new'].grid(row=i, column=2, sticky="ew", padx=ModernStyle.SPACING['lg'], pady=1, ipady=5)

        # 3. 남는 위젯 숨기기
        for i in range(target_count, len(self.row_widgets)):
            row = self.row_widgets[i]
            row['orig'].grid_forget()
            row['arrow'].grid_forget()
            row['new'].grid_forget()

    def _on_row_click(self, event, index: int):
        """행 클릭 이벤트 (다중 선택 지원)"""
        # Shift 키 확인 (범위 선택)
        if event.state & 0x0001:  # Shift
            if self.last_selected_index is not None:
                # 범위 선택
                start = min(self.last_selected_index, index)
                end = max(self.last_selected_index, index)
                self.selected_indices = set(range(start, end + 1))
            else:
                self.selected_indices = {index}
                self.last_selected_index = index
        # Ctrl 키 확인 (토글 선택)
        elif event.state & 0x0004:  # Ctrl
            if index in self.selected_indices:
                self.selected_indices.remove(index)
            else:
                self.selected_indices.add(index)
            self.last_selected_index = index
        # 일반 클릭 (단일 선택)
        else:
            self.selected_indices = {index}
            self.last_selected_index = index
        
        # 선택된 행들의 배경색 업데이트
        self._update_selection_highlight()

    def _update_selection_highlight(self):
        """선택된 행들의 하이라이트 업데이트"""
        style = ModernStyle.get_table_style()
        for i, row in enumerate(self.row_widgets):
            # 화면에 표시된 위젯만 업데이트
            if not row['orig'].winfo_ismapped():
                continue
                
            if i in self.selected_indices:
                # 선택된 행
                bg_color = style['row_selected']
                for widget in [row['orig'], row['arrow'], row['new']]:
                    widget.configure(fg_color=bg_color)
            else:
                # 선택되지 않은 행 (원래 배경색)
                bg_color = row['bg']
                for widget in [row['orig'], row['arrow'], row['new']]:
                    widget.configure(fg_color=bg_color)

    def get_selected_index(self) -> Optional[int]:
        """현재 선택된 항목의 인덱스 반환 (첫 번째 선택)"""
        if self.selected_indices:
            return min(self.selected_indices)
        return None
    
    def get_selected_indices(self) -> List[int]:
        """선택된 모든 항목의 인덱스 반환"""
        return sorted(list(self.selected_indices))

    def set_selection(self, index: int):
        """특정 인덱스 선택 (추가)"""
        if 0 <= index < len(self.row_widgets):
            self.selected_indices.add(index)
            self.last_selected_index = index
            self._update_selection_highlight()

    def set_selected_indices(self, indices: List[int]):
        """여러 인덱스 선택 (기존 선택 덮어쓰기)"""
        valid_indices = {i for i in indices if 0 <= i < len(self.row_widgets)}
        self.selected_indices = valid_indices
        if valid_indices:
            self.last_selected_index = min(valid_indices)
        else:
            self.last_selected_index = None
        self._update_selection_highlight()

    def clear_selection(self):
        """선택 초기화"""
        self.selected_indices.clear()
        self.last_selected_index = None
        self._update_selection_highlight()

    def clear(self):
        """미리보기 초기화"""
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        self.empty_label = ctk.CTkLabel(
            self.list_frame,
            text="표시할 파일이 없습니다.",
            font=ModernStyle.create_font('body'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.empty_label.pack(pady=ModernStyle.SPACING['xl'])
        self.row_widgets = []
        self.selected_indices.clear()
        self.last_selected_index = None
