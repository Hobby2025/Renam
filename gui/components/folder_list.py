"""
Folder List Component
하위 폴더 리스트 UI 컴포넌트 (단일 책임: 하위 폴더 목록 및 개별 액션)
"""

import customtkinter as ctk
from typing import Optional, Callable, List, Dict
from gui.modern_style import ModernStyle


class FolderList(ctk.CTkFrame):
    """
    폴더 리스트 컴포넌트
    책임: 하위 폴더를 수직 리스트로 표시하고 각 폴더마다 액션 버튼 제공
    """

    def __init__(self, parent,
                 on_folder_selected: Optional[Callable] = None,
                 on_execute: Optional[Callable] = None,
                 on_undo: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_folder_selected: 폴더 선택 시 호출될 콜백 (folder_name: str)
            on_execute: 변경 버튼 클릭 시 호출될 콜백 (folder_name: str)
            on_undo: 되돌리기 버튼 클릭 시 호출될 콜백 (folder_name: str)
        """
        super().__init__(parent, fg_color="transparent")
        self.on_folder_selected = on_folder_selected
        self.on_execute = on_execute
        self.on_undo = on_undo

        self.folders: List[str] = []  # 폴더명 리스트
        self.current_folder: Optional[str] = None  # 현재 선택된 폴더
        self.folder_items: Dict[str, dict] = {}  # 폴더 항목 위젯 저장

        self.row_widgets: List[dict] = []

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 카드 스타일 컨테이너
        card = ctk.CTkFrame(
            self,
            **ModernStyle.get_card_style()
        )
        card.pack(fill="both", expand=True, padx=ModernStyle.SPACING['xs'],
                 pady=ModernStyle.SPACING['xs'])

        # 내부 패딩
        inner_container = ctk.CTkFrame(card, fg_color="transparent")
        inner_container.pack(fill="both", expand=True, padx=ModernStyle.SPACING['lg'],
                           pady=ModernStyle.SPACING['md'])

        # 헤더
        header_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, ModernStyle.SPACING['md']))

        ctk.CTkLabel(
            header_frame,
            text="하위 폴더",
            font=ModernStyle.create_font('body', 'bold'),
            text_color=ModernStyle.COLORS['text_primary']
        ).pack(side="left")

        # 스크롤 가능한 폴더 리스트 컨테이너
        self.list_container = ctk.CTkScrollableFrame(
            inner_container,
            fg_color="transparent"
        )
        self.list_container.pack(fill="both", expand=True)

        # 초기 메시지
        self.empty_label = ctk.CTkLabel(
            self.list_container,
            text="폴더를 선택하면 하위 폴더 목록이 표시됩니다.",
            font=ModernStyle.create_font('caption'),
            text_color=ModernStyle.COLORS['text_tertiary']
        )
        self.empty_label.pack(pady=ModernStyle.SPACING['md'])

    def set_folders(self, folder_names: List[str], undo_states: Dict[str, bool] = None):
        """
        폴더 리스트 설정

        Args:
            folder_names: 하위 폴더명 리스트
            undo_states: 각 폴더의 되돌리기 가능 여부 {folder_name: bool}
        """
        # 기존 빈 상태 라벨 숨기기
        if hasattr(self, 'empty_label') and self.empty_label.winfo_exists():
            self.empty_label.pack_forget()

        # 기존 행 숨기기 (위젯은 재사용)
        for row in self.row_widgets:
            row['frame'].pack_forget()

        self.folders = folder_names
        self.folder_items = {}
        self.current_folder = None

        if not folder_names:
            if hasattr(self, 'empty_label') and self.empty_label.winfo_exists():
                self.empty_label.configure(
                    text="하위 폴더가 없습니다.",
                    font=ModernStyle.create_font('caption'),
                    text_color=ModernStyle.COLORS['text_tertiary']
                )
            else:
                self.empty_label = ctk.CTkLabel(
                    self.list_container,
                    text="하위 폴더가 없습니다.",
                    font=ModernStyle.create_font('caption'),
                    text_color=ModernStyle.COLORS['text_tertiary']
                )
            self.empty_label.pack(pady=ModernStyle.SPACING['md'])
            return

        if undo_states is None:
            undo_states = {}

        # 필요한 만큼 행 위젯 생성 또는 재사용
        for index, folder_name in enumerate(folder_names):
            undo_enabled = undo_states.get(folder_name, False)

            if index < len(self.row_widgets):
                row = self.row_widgets[index]
                item_frame = row['frame']
                name_label = row['name_label']
            else:
                item_frame = ctk.CTkFrame(
                    self.list_container,
                    fg_color=ModernStyle.COLORS['surface'],
                    corner_radius=ModernStyle.RADIUS['sm'],
                    cursor="hand2"
                )
                content = ctk.CTkFrame(item_frame, fg_color="transparent")
                content.pack(fill="x", padx=ModernStyle.SPACING['sm'],
                            pady=ModernStyle.SPACING['sm'])

                name_label = ctk.CTkLabel(
                    content,
                    text=folder_name,
                    font=ModernStyle.create_font('micro'),
                    text_color=ModernStyle.COLORS['text_primary'],
                    anchor="w"
                )
                name_label.pack(side="left", fill="x", expand=True)

                row = {
                    'frame': item_frame,
                    'name_label': name_label,
                }
                self.row_widgets.append(row)

            # 이벤트 및 텍스트 재설정
            item_frame.bind("<Button-1>", lambda e, name=folder_name: self.select_folder(name))
            name_label.configure(
                text=folder_name,
                font=ModernStyle.create_font('micro'),
                text_color=ModernStyle.COLORS['text_primary'],
                anchor="w"
            )
            name_label.bind("<Button-1>", lambda e, name=folder_name: self.select_folder(name))

            item_frame.pack(fill="x", pady=ModernStyle.SPACING['xs'])

            # 항목 정보 저장
            self.folder_items[folder_name] = {
                'frame': item_frame,
                'name_label': name_label,
                'undo_enabled': undo_enabled
            }

        # 첫 번째 폴더 선택
        if folder_names:
            self.select_folder(folder_names[0])

    def _create_folder_item(self, folder_name: str, undo_enabled: bool = False):
        """
        폴더 항목 생성

        Args:
            folder_name: 폴더명
            undo_enabled: 되돌리기 버튼 활성화 여부
        """
        # 항목 컨테이너 (클릭 가능)
        item_frame = ctk.CTkFrame(
            self.list_container,
            fg_color=ModernStyle.COLORS['surface'],
            corner_radius=ModernStyle.RADIUS['sm'],
            cursor="hand2"
        )
        item_frame.pack(fill="x", pady=ModernStyle.SPACING['xs'])

        # 클릭 이벤트
        item_frame.bind("<Button-1>", lambda e: self.select_folder(folder_name))

        # 내용 컨테이너
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=ModernStyle.SPACING['sm'],
                    pady=ModernStyle.SPACING['sm'])

        # 좌측: 폴더명만 표시 (버튼 없음)
        name_label = ctk.CTkLabel(
            content,
            text=folder_name,
            font=ModernStyle.create_font('micro'),
            text_color=ModernStyle.COLORS['text_primary'],
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        name_label.bind("<Button-1>", lambda e: self.select_folder(folder_name))

        # 항목 정보 저장
        self.folder_items[folder_name] = {
            'frame': item_frame,
            'name_label': name_label,
            'undo_enabled': undo_enabled
        }

    def _on_execute_click(self, folder_name: str):
        """변경 버튼 클릭 핸들러"""
        if self.on_execute:
            self.on_execute(folder_name)

    def _on_undo_click(self, folder_name: str):
        """되돌리기 버튼 클릭 핸들러"""
        if folder_name in self.folder_items and self.folder_items[folder_name]['undo_enabled']:
            if self.on_undo:
                self.on_undo(folder_name)

    def select_folder(self, folder_name: str):
        """
        폴더 선택

        Args:
            folder_name: 선택할 폴더명
        """
        if folder_name not in self.folder_items:
            return

        self.current_folder = folder_name

        # 모든 항목 스타일 업데이트
        for name, item in self.folder_items.items():
            if name == folder_name:
                # 선택된 항목
                item['frame'].configure(
                    fg_color=ModernStyle.COLORS['accent_blue'],
                    border_width=2,
                    border_color=ModernStyle.COLORS['accent_blue_dark']
                )
                item['name_label'].configure(
                    text_color=ModernStyle.COLORS['text_button'],
                    font=ModernStyle.create_font('micro', 'bold')
                )
            else:
                # 비선택 항목
                item['frame'].configure(
                    fg_color=ModernStyle.COLORS['surface'],
                    border_width=0
                )
                item['name_label'].configure(
                    text_color=ModernStyle.COLORS['text_primary'],
                    font=ModernStyle.create_font('micro')
                )

        # 콜백 호출
        if self.on_folder_selected:
            self.on_folder_selected(folder_name)

    def enable_undo(self, folder_name: str):
        """
        특정 폴더의 되돌리기 버튼 활성화

        Args:
            folder_name: 폴더명
        """
        if folder_name in self.folder_items:
            item = self.folder_items[folder_name]
            item['undo_enabled'] = True
            if 'undo_btn' in item:
                item['undo_btn'].configure(
                    state="normal",
                    fg_color=ModernStyle.COLORS['button_warning'],
                    text_color=ModernStyle.COLORS['text_button'],
                    hover_color=ModernStyle.COLORS['button_warning_hover']
                )

    def disable_undo(self, folder_name: str):
        """
        특정 폴더의 되돌리기 버튼 비활성화

        Args:
            folder_name: 폴더명
        """
        if folder_name in self.folder_items:
            item = self.folder_items[folder_name]
            item['undo_enabled'] = False
            if 'undo_btn' in item:
                item['undo_btn'].configure(
                    state="disabled",
                    fg_color=ModernStyle.COLORS['button_secondary'],
                    text_color=ModernStyle.COLORS['text_disabled'],
                    hover_color=ModernStyle.COLORS['button_secondary']
                )

    def get_current_folder(self) -> Optional[str]:
        """현재 선택된 폴더 반환"""
        return self.current_folder

    def clear(self):
        """폴더 리스트 초기화"""
        self.set_folders([])
