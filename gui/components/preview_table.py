"""
Preview Table Component
미리보기 테이블 UI 컴포넌트 (단일 책임: 파일 목록 미리보기 UI)
"""

from tkinter import Frame, Label, Button, Listbox, Scrollbar
from typing import List, Optional, Callable
from gui.modern_style import ModernStyle
from models.file_item import FileItem


class PreviewTable(Frame):
    """
    미리보기 테이블 컴포넌트
    책임: 파일 목록 표시 및 순서 변경 UI
    """

    def __init__(self, parent, on_move_up: Optional[Callable] = None,
                 on_move_down: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_move_up: 위로 이동 버튼 클릭 시 호출될 콜백
            on_move_down: 아래로 이동 버튼 클릭 시 호출될 콜백
        """
        super().__init__(parent, **ModernStyle.get_frame_style())
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down

        self.file_listbox: Optional[Listbox] = None

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 컨테이너
        container = Frame(self, **ModernStyle.get_frame_style())
        container.pack(fill="both", expand=True, padx=ModernStyle.SPACING['xl'],
                      pady=ModernStyle.SPACING['md'])

        # 헤더
        Label(
            container,
            text="미리보기",
            font=ModernStyle.create_font('body', 'bold'),
            **ModernStyle.get_label_style('primary')
        ).pack(anchor="w", pady=(0, ModernStyle.SPACING['sm']))

        # 테이블 프레임
        table_frame = Frame(container, **ModernStyle.get_frame_style())
        table_frame.pack(fill="both", expand=True)

        # 좌측: 파일 목록
        list_frame = Frame(table_frame, **ModernStyle.get_frame_style())
        list_frame.pack(side="left", fill="both", expand=True)

        # 헤더
        header_frame = Frame(list_frame, bg=ModernStyle.COLORS['surface_secondary'])
        header_frame.pack(fill="x")

        Label(
            header_frame,
            text="원본 파일명",
            width=35,
            anchor="w",
            font=ModernStyle.create_font('caption', 'bold'),
            bg=ModernStyle.COLORS['surface_secondary'],
            fg=ModernStyle.COLORS['text_secondary']
        ).pack(side="left", fill="x", expand=True, padx=ModernStyle.SPACING['sm'],
               pady=ModernStyle.SPACING['xs'])

        Label(
            header_frame,
            text="→",
            width=3,
            anchor="center",
            font=ModernStyle.create_font('caption', 'bold'),
            bg=ModernStyle.COLORS['surface_secondary'],
            fg=ModernStyle.COLORS['text_secondary']
        ).pack(side="left")

        Label(
            header_frame,
            text="변경 파일명",
            width=35,
            anchor="w",
            font=ModernStyle.create_font('caption', 'bold'),
            bg=ModernStyle.COLORS['surface_secondary'],
            fg=ModernStyle.COLORS['text_secondary']
        ).pack(side="left", fill="x", expand=True, padx=ModernStyle.SPACING['sm'],
               pady=ModernStyle.SPACING['xs'])

        # 리스트박스와 스크롤바
        listbox_frame = Frame(list_frame, **ModernStyle.get_frame_style())
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=ModernStyle.create_font('body'),
            **ModernStyle.get_listbox_style()
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 우측: 순서 변경 버튼
        button_frame = Frame(table_frame, **ModernStyle.get_frame_style())
        button_frame.pack(side="right", fill="y", padx=(ModernStyle.SPACING['md'], 0))

        Label(
            button_frame,
            text="순서\n변경",
            font=ModernStyle.create_font('caption', 'bold'),
            **ModernStyle.get_label_style('secondary')
        ).pack(pady=(0, ModernStyle.SPACING['sm']))

        # 위로 버튼
        Button(
            button_frame,
            text="↑",
            width=3,
            font=ModernStyle.create_font('body', 'bold'),
            command=lambda: self.on_move_up() if self.on_move_up else None,
            cursor="hand2",
            **ModernStyle.get_button_style('secondary')
        ).pack(pady=ModernStyle.SPACING['xs'])

        # 아래로 버튼
        Button(
            button_frame,
            text="↓",
            width=3,
            font=ModernStyle.create_font('body', 'bold'),
            command=lambda: self.on_move_down() if self.on_move_down else None,
            cursor="hand2",
            **ModernStyle.get_button_style('secondary')
        ).pack(pady=ModernStyle.SPACING['xs'])

    def update_preview(self, file_items: List[FileItem]):
        """
        미리보기 업데이트

        Args:
            file_items: 파일 아이템 리스트
        """
        if not self.file_listbox:
            return

        self.file_listbox.delete(0, "end")

        for item in file_items:
            display = f"{item.original_name:<40} → {item.new_name}"
            self.file_listbox.insert("end", display)

    def get_selected_index(self) -> Optional[int]:
        """
        현재 선택된 항목의 인덱스 반환

        Returns:
            선택된 인덱스 또는 None
        """
        if not self.file_listbox:
            return None

        selection = self.file_listbox.curselection()
        return selection[0] if selection else None

    def set_selection(self, index: int):
        """
        특정 인덱스 선택

        Args:
            index: 선택할 인덱스
        """
        if not self.file_listbox:
            return

        self.file_listbox.selection_clear(0, "end")
        self.file_listbox.selection_set(index)
        self.file_listbox.see(index)

    def clear(self):
        """미리보기 초기화"""
        if self.file_listbox:
            self.file_listbox.delete(0, "end")
