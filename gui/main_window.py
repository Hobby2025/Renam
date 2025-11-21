"""
Main Window GUI Module
GUI 메인 윈도우 (단일 책임: 컴포넌트 조립 및 이벤트 조정)
"""

from pathlib import Path
from tkinter import Tk, Frame, messagebox
from typing import List, Optional

from models.file_item import FileItem
from core.sorter import FileSorter
from core.name_generator import NameGenerator
from core.file_operations import FileOperations
from core.undo_manager import UndoManager

from gui.modern_style import ModernStyle
from gui.components import (
    FolderSelector,
    SortOptions,
    PatternInput,
    PreviewTable,
    ActionButtons
)


class RenamMainWindow:
    """
    Renam 메인 윈도우 클래스
    책임: UI 컴포넌트 조립 및 이벤트 조정 (오케스트레이션)
    """

    def __init__(self, root: Tk):
        """
        메인 윈도우 초기화

        Args:
            root: Tkinter 루트 윈도우
        """
        self.root = root
        self.root.title("Renam 📁✨")
        self.root.geometry("1000x750")
        self.root.configure(bg=ModernStyle.COLORS['background'])

        # 데이터
        self.current_folder: Optional[Path] = None
        self.file_items: List[FileItem] = []

        # 비즈니스 로직 컴포넌트
        self.undo_manager = UndoManager()

        # UI 컴포넌트
        self.folder_selector: Optional[FolderSelector] = None
        self.sort_options: Optional[SortOptions] = None
        self.pattern_input: Optional[PatternInput] = None
        self.preview_table: Optional[PreviewTable] = None
        self.action_buttons: Optional[ActionButtons] = None

        self._setup_ui()

    def _setup_ui(self):
        """UI 전체 구성"""
        # 메인 컨테이너
        main_container = Frame(self.root, bg=ModernStyle.COLORS['background'])
        main_container.pack(fill="both", expand=True)

        # 스크롤 가능한 콘텐츠 영역
        content_frame = Frame(main_container, bg=ModernStyle.COLORS['surface'])
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # 컴포넌트 생성 및 배치
        self.folder_selector = FolderSelector(
            content_frame,
            on_folder_selected=self._on_folder_selected
        )
        self.folder_selector.pack(fill="x")

        self.sort_options = SortOptions(
            content_frame,
            on_sort_changed=self._on_sort_changed
        )
        self.sort_options.pack(fill="x")

        self.pattern_input = PatternInput(content_frame)
        self.pattern_input.pack(fill="x")

        self.preview_table = PreviewTable(
            content_frame,
            on_move_up=self._on_move_up,
            on_move_down=self._on_move_down
        )
        self.preview_table.pack(fill="both", expand=True)

        self.action_buttons = ActionButtons(
            content_frame,
            on_execute=self._on_execute,
            on_undo=self._on_undo,
            on_quit=self.root.quit
        )
        self.action_buttons.pack(fill="x")

    # ==================== 이벤트 핸들러 ====================

    def _on_folder_selected(self, folder: Path):
        """폴더 선택 이벤트 핸들러"""
        self.current_folder = folder
        self._scan_and_load_files()

    def _scan_and_load_files(self):
        """폴더 스캔 및 파일 로드"""
        is_valid, error_msg = FileOperations.validate_folder(self.current_folder)
        if not is_valid:
            messagebox.showerror("오류", error_msg)
            return

        try:
            self.file_items = FileOperations.scan_folder(self.current_folder)
        except Exception as e:
            messagebox.showerror("오류", f"파일 스캔 중 오류 발생:\n{str(e)}")
            return

        if not self.file_items:
            messagebox.showwarning("경고", "선택한 폴더에 이미지 파일이 없습니다.")
            return

        self._apply_sort()
        messagebox.showinfo("완료", f"{len(self.file_items)}개의 이미지 파일을 찾았습니다.")

    def _on_sort_changed(self):
        """정렬 규칙 변경 이벤트 핸들러"""
        if self.file_items:
            self._apply_sort()

    def _apply_sort(self):
        """정렬 적용"""
        if not self.file_items:
            return

        mode = self.sort_options.get_sort_mode()

        try:
            if mode == 1:  # 숫자
                self.file_items = FileSorter.sort_by_numeric(self.file_items)
            elif mode == 2:  # 알파벳
                self.file_items = FileSorter.sort_by_alphabetic(self.file_items)
            elif mode == 3:  # 날짜
                self.file_items = FileSorter.sort_by_date(self.file_items)
            elif mode == 4:  # 확장자
                self.file_items = FileSorter.sort_by_extension(self.file_items)
            elif mode == 5:  # 정규식
                pattern = self.sort_options.get_regex_pattern()
                self.file_items = FileSorter.sort_by_regex(self.file_items, pattern)

            FileSorter.update_order(self.file_items)
            self._update_preview()

        except Exception as e:
            messagebox.showerror("정렬 오류", f"정렬 중 오류가 발생했습니다:\n{str(e)}")

    def _update_preview(self):
        """미리보기 업데이트"""
        pattern = self.pattern_input.get_pattern()

        for i, item in enumerate(self.file_items):
            new_name = NameGenerator.generate(i + 1, pattern, item.ext)
            item.new_name = new_name

        self.preview_table.update_preview(self.file_items)

    def _on_move_up(self):
        """항목 위로 이동 이벤트 핸들러"""
        index = self.preview_table.get_selected_index()
        if index is None:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        if index == 0:
            return  # 이미 최상단

        # 교환
        self.file_items[index], self.file_items[index - 1] = \
            self.file_items[index - 1], self.file_items[index]

        self._update_preview()
        self.preview_table.set_selection(index - 1)

    def _on_move_down(self):
        """항목 아래로 이동 이벤트 핸들러"""
        index = self.preview_table.get_selected_index()
        if index is None:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        if index >= len(self.file_items) - 1:
            return  # 이미 최하단

        # 교환
        self.file_items[index], self.file_items[index + 1] = \
            self.file_items[index + 1], self.file_items[index]

        self._update_preview()
        self.preview_table.set_selection(index + 1)

    def _on_execute(self):
        """파일명 변경 실행 이벤트 핸들러"""
        if not self.file_items:
            messagebox.showwarning("경고", "파일이 없습니다.")
            return

        # 중복 체크
        new_names = [item.new_name for item in self.file_items]
        if NameGenerator.check_duplicates(new_names):
            messagebox.showerror("오류", "중복된 파일명이 발생합니다. 패턴을 수정하세요.")
            return

        # 확인
        result = messagebox.askyesno(
            "확인",
            f"{len(self.file_items)}개의 파일명을 변경하시겠습니까?\n"
            "이 작업은 실제 파일명을 변경합니다."
        )
        if not result:
            return

        # Undo 데이터 준비
        before_names = [item.original_name for item in self.file_items]
        after_names = [item.new_name for item in self.file_items]

        # 파일명 변경 실행
        success, error_msg = FileOperations.rename_files(
            self.current_folder, self.file_items
        )

        if not success:
            messagebox.showerror("오류", f"파일명 변경 중 오류가 발생했습니다:\n{error_msg}")
            return

        # Undo 로그 저장
        self.undo_manager.save_operation(
            self.current_folder, before_names, after_names
        )

        messagebox.showinfo("완료", f"{len(self.file_items)}개의 파일명이 변경되었습니다.")

        # 재스캔
        self._scan_and_load_files()

    def _on_undo(self):
        """파일명 변경 되돌리기 이벤트 핸들러"""
        if not self.undo_manager.has_operations():
            messagebox.showinfo("알림", "되돌릴 작업이 없습니다.")
            return

        last_op = self.undo_manager.get_last_operation()
        folder = Path(last_op["folder"])

        is_valid, error_msg = FileOperations.validate_folder(folder)
        if not is_valid:
            messagebox.showerror("오류", f"원본 폴더를 찾을 수 없습니다:\n{error_msg}")
            return

        # 확인
        result = messagebox.askyesno(
            "확인",
            f"마지막 작업을 되돌리시겠습니까?\n"
            f"폴더: {folder}\n"
            f"시간: {last_op['timestamp']}"
        )
        if not result:
            return

        # 복구 실행
        success, error_msg = FileOperations.restore_files(
            folder, last_op["before"], last_op["after"]
        )

        if not success:
            messagebox.showerror("오류", error_msg)
            return

        # 로그 제거
        self.undo_manager.remove_last_operation()
        messagebox.showinfo("완료", "파일명이 복구되었습니다.")

        # 현재 폴더가 동일하면 재스캔
        if self.current_folder == folder:
            self._scan_and_load_files()

    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()
