"""
Folder Selector Component
폴더 선택 UI 컴포넌트 (단일 책임: 폴더 선택 UI)
"""

from tkinter import Frame, Label, Button, StringVar, filedialog
from pathlib import Path
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class FolderSelector(Frame):
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
        super().__init__(parent, **ModernStyle.get_frame_style())
        self.on_folder_selected = on_folder_selected

        self.folder_var = StringVar(value="폴더를 선택하세요")
        self.selected_folder: Optional[Path] = None

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 상단 여백
        Frame(self, height=ModernStyle.SPACING['lg'], **ModernStyle.get_frame_style()).pack()

        # 컨테이너 프레임
        container = Frame(self, **ModernStyle.get_frame_style())
        container.pack(fill="x", padx=ModernStyle.SPACING['xl'])

        # 아이콘 + 레이블
        header_frame = Frame(container, **ModernStyle.get_frame_style())
        header_frame.pack(side="left")

        Label(
            header_frame,
            text="📂",
            font=ModernStyle.create_font('headline'),
            **ModernStyle.get_label_style('primary')
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        Label(
            header_frame,
            text="폴더 선택:",
            font=ModernStyle.create_font('body', 'bold'),
            **ModernStyle.get_label_style('primary')
        ).pack(side="left")

        # 선택된 폴더 표시
        self.path_label = Label(
            container,
            textvariable=self.folder_var,
            font=ModernStyle.create_font('body'),
            **ModernStyle.get_label_style('secondary'),
            anchor="w",
            width=50
        )
        self.path_label.pack(side="left", padx=ModernStyle.SPACING['md'], fill="x", expand=True)

        # 찾아보기 버튼
        browse_btn = Button(
            container,
            text="찾아보기",
            font=ModernStyle.create_font('body'),
            command=self._on_browse,
            cursor="hand2",
            **ModernStyle.get_button_style('primary')
        )
        browse_btn.pack(side="right")

        # 하단 구분선
        Frame(self, height=1, bg=ModernStyle.COLORS['separator']).pack(fill="x", pady=ModernStyle.SPACING['md'])

    def _on_browse(self):
        """폴더 찾아보기 버튼 클릭 이벤트"""
        folder = filedialog.askdirectory(title="이미지 폴더를 선택하세요")
        if folder:
            self.selected_folder = Path(folder)
            self.folder_var.set(str(self.selected_folder))

            # 콜백 호출
            if self.on_folder_selected:
                self.on_folder_selected(self.selected_folder)

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
