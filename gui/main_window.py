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
    FolderList,
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
        self.file_items: List[FileItem] = []  # 현재 탭의 파일 목록

        # 탭별 데이터 관리 (하위 폴더별로 독립적 관리)
        self.tab_data: dict = {}  # {tab_name: {'file_items': [], 'sort_mode': 1, 'pattern': '{n}'}}
        self.current_tab: Optional[str] = None
        self.subfolders: List[str] = []  # 하위 폴더 목록

        # 비즈니스 로직 컴포넌트
        self.undo_manager = UndoManager()

        # UI 컴포넌트
        self.folder_selector: Optional[FolderSelector] = None
        self.folder_list: Optional[FolderList] = None
        self.sort_options: Optional[SortOptions] = None
        self.pattern_input: Optional[PatternInput] = None
        self.preview_table: Optional[PreviewTable] = None
        self.action_buttons: Optional[ActionButtons] = None

        self._setup_ui()

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

        # 폴더 리스트 (하위 폴더 목록)
        self.folder_list = FolderList(
            left_panel,
            on_folder_selected=self._on_subfolder_selected,
            on_execute=self._on_folder_execute,
            on_undo=self._on_folder_undo
        )
        self.folder_list.pack(fill="both", expand=True, pady=(0, ModernStyle.SPACING['lg']))

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
        # - 하위 폴더 없을 때: 단일 폴더 변경
        # - 하위 폴더 있을 때: 모든 폴더 일괄 변경
        self.action_buttons = ActionButtons(
            main_container,
            on_execute=self._on_execute_all,
            on_undo=self._on_undo_all,
            on_quit=self.root.quit
        )
        # 초기에는 숨김 (폴더 선택 시 표시)
        # self.action_buttons.pack(fill="x", pady=(ModernStyle.SPACING['lg'], 0))

    # ==================== 이벤트 핸들러 ====================

    def _on_folder_selected(self, folder: Path):
        """메인 폴더 선택 이벤트 핸들러 (폴더 선택기에서)"""
        self.current_folder = folder
        self._scan_subfolders_and_setup_list()

    def _on_subfolder_selected(self, folder_name: str):
        """하위 폴더 선택 이벤트 핸들러 (폴더 리스트에서)"""
        self._show_folder(folder_name)

    def _on_folder_execute(self, folder_name: str):
        """폴더별 변경 버튼 클릭 핸들러"""
        self._execute_folder(folder_name)

    def _on_folder_undo(self, folder_name: str):
        """폴더별 되돌리기 버튼 클릭 핸들러"""
        self._undo_folder(folder_name)

    def _scan_subfolders_and_setup_list(self):
        """하위 폴더 스캔 및 리스트 설정"""
        is_valid, error_msg = FileOperations.validate_folder(self.current_folder)
        if not is_valid:
            messagebox.showerror("오류", error_msg)
            return

        # 하위 폴더 목록 가져오기
        self.subfolders = FileOperations.get_subfolders(self.current_folder)

        if not self.subfolders:
            # 하위 폴더가 없으면 현재 폴더의 파일만 스캔
            messagebox.showinfo("알림", "하위 폴더가 없습니다. 현재 폴더의 파일을 표시합니다.")
            self.folder_list.clear()
            # 하단 버튼 표시 (단일 폴더 모드)
            self.action_buttons.pack(fill="x", pady=(ModernStyle.SPACING['lg'], 0))
            self._scan_and_load_files()
            return

        # 하위 폴더가 있으면 하단 버튼은 "모든 폴더 일괄 변경" 용도
        self.action_buttons.pack(fill="x", pady=(ModernStyle.SPACING['lg'], 0))

        # 각 폴더의 데이터 초기화
        self.tab_data = {}
        total_files = 0

        for subfolder in self.subfolders:
            try:
                files = FileOperations.scan_subfolder(self.current_folder, subfolder)
                total_files += len(files)
                self.tab_data[subfolder] = {
                    'file_items': files,
                    'sort_mode': 1,  # 기본: 숫자 정렬
                    'pattern': '{n}'  # 기본: 숫자
                }
            except Exception as e:
                messagebox.showerror("오류", f"{subfolder} 스캔 중 오류:\n{str(e)}")

        # 각 폴더의 되돌리기 가능 여부 확인
        operations = self.undo_manager.get_all_operations()
        undo_states = {}
        for subfolder in self.subfolders:
            folder_path = self.current_folder / subfolder
            has_undo = any(Path(op["folder"]) == folder_path for op in operations)
            undo_states[subfolder] = has_undo

        # 폴더 리스트 설정
        self.folder_list.set_folders(self.subfolders, undo_states)

        # 첫 번째 폴더가 자동 선택되므로 하단 버튼 상태 업데이트
        if self.subfolders:
            self.current_tab = self.subfolders[0]
            self._update_bottom_undo_state()

        if total_files == 0:
            messagebox.showwarning("경고", "하위 폴더에 이미지 파일이 없습니다.")
        else:
            messagebox.showinfo("완료",
                f"{len(self.subfolders)}개의 하위 폴더에서 총 {total_files}개의 이미지 파일을 찾았습니다.")

    def _scan_and_load_files(self):
        """폴더 스캔 및 파일 로드 (하위 폴더 없을 때)"""
        try:
            self.file_items = FileOperations.scan_folder(self.current_folder)
        except Exception as e:
            messagebox.showerror("오류", f"파일 스캔 중 오류 발생:\n{str(e)}")
            return

        if not self.file_items:
            messagebox.showwarning("경고", "선택한 폴더에 이미지 파일이 없습니다.")
            return

        # 되돌리기 버튼 상태 업데이트
        self._update_single_folder_undo_state()

        self._apply_sort()
        messagebox.showinfo("완료", f"{len(self.file_items)}개의 이미지 파일을 찾았습니다.")

    def _update_single_folder_undo_state(self):
        """단일 폴더 모드의 되돌리기 버튼 상태 업데이트"""
        if not self.action_buttons:
            return

        # 현재 폴더의 undo 작업이 있는지 확인
        operations = self.undo_manager.get_all_operations()
        has_undo = any(Path(op["folder"]) == self.current_folder for op in operations)

        if has_undo:
            self.action_buttons.enable_undo()
        else:
            self.action_buttons.disable_undo()

    def _update_bottom_undo_state(self):
        """하위 폴더 모드에서 현재 선택된 폴더의 되돌리기 버튼 상태 업데이트"""
        if not self.action_buttons or not self.current_tab:
            return

        # 현재 선택된 폴더의 undo 작업이 있는지 확인
        folder_path = self.current_folder / self.current_tab
        operations = self.undo_manager.get_all_operations()
        has_undo = any(Path(op["folder"]) == folder_path for op in operations)

        if has_undo:
            self.action_buttons.enable_undo()
        else:
            self.action_buttons.disable_undo()

    def _save_current_folder_state(self):
        """현재 선택된 폴더의 상태 저장"""
        if self.current_tab and self.current_tab in self.tab_data:
            self.tab_data[self.current_tab]['file_items'] = self.file_items
            self.tab_data[self.current_tab]['sort_mode'] = self.sort_options.get_sort_mode()
            self.tab_data[self.current_tab]['pattern'] = self.pattern_input.get_pattern()

    def _show_folder(self, folder_name: str):
        """특정 폴더의 데이터 표시"""
        # 현재 폴더 상태 저장
        self._save_current_folder_state()

        if folder_name not in self.tab_data:
            return

        self.current_tab = folder_name
        folder_info = self.tab_data[folder_name]

        # 현재 폴더의 데이터를 UI에 반영
        self.file_items = folder_info['file_items']
        self.sort_options.set_sort_mode(folder_info['sort_mode'])
        self.pattern_input.set_pattern(folder_info['pattern'])

        # 하단 버튼의 되돌리기 상태 업데이트 (하위 폴더 모드일 때)
        if self.subfolders and self.tab_data:
            self._update_bottom_undo_state()

        self._update_preview()

    def _on_sort_changed(self, mode=None):
        """정렬 규칙 변경 이벤트 핸들러"""
        if self.file_items:
            self._apply_sort()
            # 현재 폴더에 정렬 모드 저장
            if self.current_tab and self.current_tab in self.tab_data:
                self.tab_data[self.current_tab]['sort_mode'] = self.sort_options.get_sort_mode()

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

            # 현재 폴더에 정렬된 파일 목록 저장
            if self.current_tab and self.current_tab in self.tab_data:
                self.tab_data[self.current_tab]['file_items'] = self.file_items

            self._update_preview()

        except Exception as e:
            messagebox.showerror("정렬 오류", f"정렬 중 오류가 발생했습니다:\n{str(e)}")

    def _update_preview(self, *args):
        """미리보기 업데이트"""
        # 미리보기 타이틀에 현재 폴더/탭 이름 표시
        folder_title = None
        if self.subfolders and self.current_tab:
            folder_title = self.current_tab
        elif self.current_folder:
            folder_title = self.current_folder.name

        if self.preview_table:
            self.preview_table.set_folder_title(folder_title)

        pattern = self.pattern_input.get_pattern()

        for i, item in enumerate(self.file_items):
            new_name = NameGenerator.generate(i + 1, pattern, item.ext)
            item.new_name = new_name

        # 현재 폴더에 패턴 저장
        if self.current_tab and self.current_tab in self.tab_data:
            self.tab_data[self.current_tab]['pattern'] = pattern

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

        # 현재 폴더에 변경된 파일 목록 저장
        if self.current_tab and self.current_tab in self.tab_data:
            self.tab_data[self.current_tab]['file_items'] = self.file_items

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

        # 현재 폴더에 변경된 파일 목록 저장
        if self.current_tab and self.current_tab in self.tab_data:
            self.tab_data[self.current_tab]['file_items'] = self.file_items

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

        # 현재 폴더에 변경된 파일 목록 저장
        if self.current_tab and self.current_tab in self.tab_data:
            self.tab_data[self.current_tab]['file_items'] = self.file_items

        self._update_preview()
        self.preview_table.clear_selection()

    def _on_reset(self):
        """목록 초기화 이벤트 핸들러 (초기 상태로 복구)"""
        if not self.file_items and not self.current_folder:
            return
            
        if messagebox.askyesno("초기화", "파일 목록과 순서를 초기 상태로 되돌리시겠습니까?"):
            # 하위 폴더(탭) 모드일 때는 현재 선택된 폴더만 재스캔
            if self.subfolders and self.tab_data and self.current_tab:
                self._rescan_folder(self.current_tab)
            elif self.current_folder and self.current_folder.exists():
                # 단일 폴더 모드: 현재 폴더 전체를 재스캔
                self._scan_and_load_files()
            else:
                # 폴더 없이 파일만 있는 경우 (드래그앤드롭 등) -> 목록 비우기
                self.file_items = []
                self._update_preview()
            
            self.preview_table.clear_selection()

    def _execute_folder(self, folder_name: str):
        """특정 폴더의 파일명 변경 실행"""
        # 하위 폴더 모드인지 확인
        if folder_name in self.tab_data:
            # 하위 폴더 모드
            folder_info = self.tab_data[folder_name]
            file_items = folder_info['file_items']
            folder_path = self.current_folder / folder_name
        else:
            # 단일 폴더 모드 (하위 폴더 없음)
            file_items = self.file_items
            folder_path = self.current_folder

        if not file_items:
            messagebox.showwarning("경고", "파일이 없습니다.")
            return

        # 패턴 적용하여 새 이름 생성 (최신 데이터 반영)
        if folder_name in self.tab_data:
            pattern = self.tab_data[folder_name]['pattern']
            for i, item in enumerate(file_items):
                new_name = NameGenerator.generate(i + 1, pattern, item.ext)
                item.new_name = new_name

        # 중복 체크
        new_names = [item.new_name for item in file_items]
        if NameGenerator.check_duplicates(new_names):
            messagebox.showerror("오류", "중복된 파일명이 발생합니다. 패턴을 수정하세요.")
            return

        # 확인
        result = messagebox.askyesno(
            "확인",
            f"'{folder_name}' 폴더의 {len(file_items)}개 파일명을 변경하시겠습니까?\n"
            "이 작업은 실제 파일명을 변경합니다."
        )
        if not result:
            return

        # Undo 데이터 준비
        before_names = [item.original_name for item in file_items]
        after_names = [item.new_name for item in file_items]

        # 파일명 변경 실행
        success, error_msg = FileOperations.rename_files(folder_path, file_items)

        if not success:
            messagebox.showerror("오류", f"파일명 변경 중 오류가 발생했습니다:\n{error_msg}")
            return

        # Undo 로그 저장
        self.undo_manager.save_operation(folder_path, before_names, after_names)

        # 되돌리기 버튼 활성화
        if folder_name in self.tab_data:
            # 하위 폴더 모드 - 폴더 리스트의 버튼 활성화
            self.folder_list.enable_undo(folder_name)
        else:
            # 단일 폴더 모드 - 하단 버튼 활성화
            self.action_buttons.enable_undo()

        messagebox.showinfo("완료", f"'{folder_name}' 폴더의 {len(file_items)}개 파일명이 변경되었습니다.")

        # 해당 폴더 재스캔
        self._rescan_folder(folder_name)

    def _undo_folder(self, folder_name: str):
        """특정 폴더의 되돌리기 실행"""
        # 해당 폴더의 가장 최근 작업 찾기
        folder_path = self.current_folder / folder_name if folder_name in self.tab_data else self.current_folder

        # 해당 폴더의 작업이 있는지 확인
        operations = self.undo_manager.get_all_operations()
        last_op = None
        last_op_index = None
        for i, op in enumerate(reversed(operations)):
            if Path(op["folder"]) == folder_path:
                last_op = op
                last_op_index = len(operations) - 1 - i
                break

        if not last_op:
            messagebox.showinfo("알림", f"'{folder_name}' 폴더의 되돌릴 작업이 없습니다.")
            return

        # 확인
        result = messagebox.askyesno(
            "확인",
            f"'{folder_name}' 폴더의 마지막 작업을 되돌리시겠습니까?\n"
            f"시간: {last_op['timestamp']}"
        )
        if not result:
            return

        # 복구 실행
        success, error_msg = FileOperations.restore_files(
            folder_path, last_op["before"], last_op["after"]
        )

        if not success:
            messagebox.showerror("오류", error_msg)
            return

        # 해당 작업만 로그에서 제거
        operations.pop(last_op_index)
        self.undo_manager._save_logs(operations)

        # 해당 폴더에 더 이상 작업이 없으면 버튼 비활성화
        has_more = any(Path(op["folder"]) == folder_path for op in operations)
        if not has_more:
            if folder_name in self.tab_data:
                # 하위 폴더 모드
                self.folder_list.disable_undo(folder_name)
            else:
                # 단일 폴더 모드
                self.action_buttons.disable_undo()

        messagebox.showinfo("완료", f"'{folder_name}' 폴더의 파일명이 복구되었습니다.")

        # 해당 폴더 재스캔
        self._rescan_folder(folder_name)

    def _rescan_folder(self, folder_name: str):
        """특정 폴더 재스캔"""
        if folder_name in self.tab_data:
            # 하위 폴더 모드
            try:
                files = FileOperations.scan_subfolder(self.current_folder, folder_name)
                self.tab_data[folder_name]['file_items'] = files

                # 현재 선택된 폴더라면 UI 업데이트
                if self.current_tab == folder_name:
                    self.file_items = files
                    # 하위 폴더 모드에서도 현재 선택된 정렬 규칙 재적용
                    self._apply_sort()

                # 되돌리기 버튼 상태 업데이트
                folder_path = self.current_folder / folder_name
                operations = self.undo_manager.get_all_operations()
                has_undo = any(Path(op["folder"]) == folder_path for op in operations)
                if has_undo:
                    self.folder_list.enable_undo(folder_name)
                else:
                    self.folder_list.disable_undo(folder_name)

            except Exception as e:
                messagebox.showerror("오류", f"폴더 재스캔 중 오류:\n{str(e)}")
        else:
            # 단일 폴더 모드
            self._scan_and_load_files()

    def _on_execute_all(self):
        """하단 변경 버튼 - 현재 선택된 폴더 또는 단일 폴더 변경"""
        # 하위 폴더가 있는지 확인
        if not self.subfolders or not self.tab_data:
            # 단일 폴더 모드 - 모든 파일 처리
            if self.current_folder:
                self._execute_folder(self.current_folder.name)
            return

        # 하위 폴더 모드 - 현재 선택된 탭(폴더)만 처리
        if not self.current_tab:
            messagebox.showwarning("경고", "폴더를 선택해주세요.")
            return

        # 현재 탭의 폴더만 실행
        self._execute_folder(self.current_tab)

    def _on_undo_all(self):
        """하단 되돌리기 버튼 - 현재 선택된 폴더 또는 단일 폴더 되돌리기"""
        # 하위 폴더가 있는지 확인
        if not self.subfolders or not self.tab_data:
            # 단일 폴더 모드 - 모든 파일 되돌리기
            if self.current_folder:
                self._undo_folder(self.current_folder.name)
            return

        # 하위 폴더 모드 - 현재 선택된 탭(폴더)만 되돌리기
        if not self.current_tab:
            messagebox.showwarning("경고", "폴더를 선택해주세요.")
            return

        # 현재 탭의 폴더만 되돌리기
        self._undo_folder(self.current_tab)

    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()
