"""
Main Window GUI Module
GUI 메인 윈도우 (단일 책임: 컴포넌트 조립 및 이벤트 조정)
"""

from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
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

    def __init__(self, root: ctk.CTk):
        """
        메인 윈도우 초기화

        Args:
            root: CustomTkinter 루트 윈도우
        """
        self.root = root
        self.root.title("RENAM | 리넴")
        self.root.geometry("1150x700")  # 최적화된 사이즈
        self.root.resizable(False, False)  # 창 크기 고정

        # 배경색 설정 (웹 스타일)
        self.root.configure(fg_color=ModernStyle.COLORS['background'])

        # 아이콘 설정
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                # 창 아이콘 설정
                self.root.iconbitmap(str(icon_path))
                
                # Windows 작업표시줄 아이콘 설정 (Python 실행시에도 커스텀 아이콘 표시)
                try:
                    import ctypes
                    myappid = 'renam.filerenamer.1.0'  # 임의의 앱 ID
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                except Exception:
                    pass
        except Exception:
            pass  # 아이콘 없어도 계속 실행

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

    def _update_undo_button_state(self):
        """되돌리기 버튼 상태 업데이트"""
        if not self.action_buttons:
            return

        if self.undo_manager.has_operations():
            self.action_buttons.enable_undo()
        else:
            self.action_buttons.disable_undo()

    def _setup_ui(self):
        """UI 전체 구성 (웹 스타일)"""
        # 메인 컨테이너
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=ModernStyle.SPACING['lg'],
                           pady=ModernStyle.SPACING['lg'])

        # 1. 상단: 폴더 선택
        self.folder_selector = FolderSelector(
            main_container,
            on_folder_selected=self._on_folder_selected
        )
        self.folder_selector.pack(fill="x", pady=(0, ModernStyle.SPACING['lg']))

        # 2. 중앙: 2단 레이아웃 (좌: 설정, 우: 미리보기)
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # 좌측 패널 (설정)
        left_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_panel.pack(side="left", fill="y", padx=(0, ModernStyle.SPACING['lg']), anchor="n")

        # 우측 패널 (미리보기)
        self.right_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.right_panel.pack(side="left", fill="both", expand=True)

        # 좌측 패널 컴포넌트
        self.sort_options = SortOptions(
            left_panel,
            on_sort_changed=self._on_sort_changed
        )
        self.sort_options.pack(fill="x", pady=(0, ModernStyle.SPACING['lg']))

        self.pattern_input = PatternInput(
            left_panel,
            on_pattern_changed=self._update_preview
        )
        self.pattern_input.pack(fill="x")

        # 우측 패널 컴포넌트
        self.preview_table = PreviewTable(
            self.right_panel,
            on_move_up=self._on_move_up,
            on_move_down=self._on_move_down,
            on_remove=self._on_remove,
            on_reset=self._on_reset
        )
        self.preview_table.pack(fill="both", expand=True)

        # 3. 하단: 실행 버튼
        self.action_buttons = ActionButtons(
            main_container,
            on_execute=self._on_execute,
            on_undo=self._on_undo,
            on_quit=self.root.quit
        )
        self.action_buttons.pack(fill="x", pady=(ModernStyle.SPACING['lg'], 0))

        # 초기 버튼 상태 설정
        self._update_undo_button_state()

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

    def _on_sort_changed(self, mode=None):
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

    def _update_preview(self, *args):
        """미리보기 업데이트"""
        pattern = self.pattern_input.get_pattern()

        for i, item in enumerate(self.file_items):
            new_name = NameGenerator.generate(i + 1, pattern, item.ext)
            item.new_name = new_name

        self.preview_table.update_preview(self.file_items)

    def _on_move_up(self):
        """항목 위로 이동 (블록 이동 알고리즘)"""
        indices = self.preview_table.get_selected_indices()
        if not indices:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        # 이미 최상단에 포함되어 있으면 이동 불가
        if 0 in indices:
            return

        # 선택된 항목과 선택되지 않은 항목 분리
        selected_items = [self.file_items[i] for i in indices]
        remaining_items = [item for i, item in enumerate(self.file_items) if i not in indices]

        # 삽입 위치 계산 (가장 위의 선택 항목 인덱스 - 1)
        target_idx = max(0, indices[0] - 1)

        # 리스트 재구성
        self.file_items = remaining_items[:target_idx] + selected_items + remaining_items[target_idx:]

        self._update_preview()
        
        # 선택 상태 업데이트 (이동된 위치로)
        new_indices = list(range(target_idx, target_idx + len(selected_items)))
        self.preview_table.set_selected_indices(new_indices)

    def _on_move_down(self):
        """항목 아래로 이동 (블록 이동 알고리즘)"""
        indices = self.preview_table.get_selected_indices()
        if not indices:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        # 이미 최하단에 포함되어 있으면 이동 불가
        if len(self.file_items) - 1 in indices:
            return

        # 선택된 항목과 선택되지 않은 항목 분리
        selected_items = [self.file_items[i] for i in indices]
        remaining_items = [item for i, item in enumerate(self.file_items) if i not in indices]

        # 삽입 위치 계산
        # (가장 아래 선택 항목 인덱스) - (선택된 개수) + 2
        # 예: [A, B, C], B(1) 선택. 남은거 [A, C]. target = 1 - 1 + 2 = 2. [A, C] 뒤에 B 삽입 -> [A, C, B]
        target_idx = min(len(remaining_items), indices[-1] - len(indices) + 2)

        # 리스트 재구성
        self.file_items = remaining_items[:target_idx] + selected_items + remaining_items[target_idx:]

        self._update_preview()
        
        # 선택 상태 업데이트 (이동된 위치로)
        new_indices = list(range(target_idx, target_idx + len(selected_items)))
        self.preview_table.set_selected_indices(new_indices)

    def _on_remove(self):
        """항목 제거 이벤트 핸들러"""
        indices = self.preview_table.get_selected_indices()
        if not indices:
            messagebox.showinfo("알림", "제거할 항목을 선택하세요.")
            return

        # 뒤에서부터 제거해야 인덱스가 꼬이지 않음
        for index in sorted(indices, reverse=True):
            del self.file_items[index]

        self._update_preview()
        self.preview_table.clear_selection()

    def _on_reset(self):
        """목록 초기화 이벤트 핸들러 (초기 상태로 복구)"""
        if not self.file_items and not self.current_folder:
            return
            
        if messagebox.askyesno("초기화", "파일 목록과 순서를 초기 상태로 되돌리시겠습니까?"):
            if self.current_folder and self.current_folder.exists():
                # 폴더가 선택된 상태라면 재스캔 (원래대로 복구)
                self._scan_and_load_files()
            else:
                # 폴더 없이 파일만 있는 경우 (드래그앤드롭 등) -> 목록 비우기
                self.file_items = []
                self._update_preview()
            
            self.preview_table.clear_selection()

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

        # 되돌리기 버튼 활성화
        self.action_buttons.enable_undo()

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

        # 더 이상 되돌릴 작업이 없으면 버튼 비활성화
        if not self.undo_manager.has_operations():
            self.action_buttons.disable_undo()

        messagebox.showinfo("완료", "파일명이 복구되었습니다.")

        # 현재 폴더가 동일하면 재스캔
        if self.current_folder == folder:
            self._scan_and_load_files()

    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()
