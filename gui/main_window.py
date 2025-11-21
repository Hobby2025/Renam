"""
Main Window GUI Module
GUI 컴포넌트 (단일 책임: 사용자 인터페이스 표시 및 이벤트 처리)
"""

from pathlib import Path
from tkinter import (
    Tk, Label, Button, Entry, Frame, Listbox,
    Scrollbar, StringVar, IntVar, Radiobutton,
    messagebox, filedialog
)
from typing import List, Optional

from models.file_item import FileItem
from core.sorter import FileSorter
from core.name_generator import NameGenerator
from core.file_operations import FileOperations
from core.undo_manager import UndoManager


class RenamMainWindow:
    """
    Renam 메인 윈도우 클래스
    책임: GUI 표시 및 사용자 인터랙션 처리
    """

    def __init__(self, root: Tk):
        """
        메인 윈도우 초기화

        Args:
            root: Tkinter 루트 윈도우
        """
        self.root = root
        self.root.title("Renam 📁✨")
        self.root.geometry("900x700")

        # 데이터
        self.current_folder: Optional[Path] = None
        self.file_items: List[FileItem] = []

        # 컴포넌트
        self.undo_manager = UndoManager()

        # GUI 변수
        self.folder_var = StringVar(value="폴더를 선택하세요")
        self.sort_mode = IntVar(value=1)  # 1: 숫자, 2: 알파벳, 3: 날짜, 4: 확장자, 5: 정규식
        self.regex_pattern = StringVar(value=r"(\d+)")
        self.name_pattern = StringVar(value="{n}")

        # UI 구성
        self._setup_ui()

    def _setup_ui(self):
        """UI 전체 구성"""
        self._create_folder_selector()
        self._create_sort_options()
        self._create_pattern_input()
        self._create_preview_table()
        self._create_action_buttons()

    def _create_folder_selector(self):
        """폴더 선택 섹션 생성"""
        folder_frame = Frame(self.root, padx=10, pady=10)
        folder_frame.pack(fill="x")

        Label(folder_frame, text="📂 폴더 선택:", font=("Arial", 10)).pack(side="left")
        Label(folder_frame, textvariable=self.folder_var, relief="sunken", width=50).pack(
            side="left", padx=5
        )
        Button(folder_frame, text="찾아보기", command=self._on_select_folder).pack(side="left")

    def _create_sort_options(self):
        """정렬 규칙 섹션 생성"""
        sort_frame = Frame(self.root, padx=10, pady=5)
        sort_frame.pack(fill="x")

        Label(sort_frame, text="정렬 규칙:", font=("Arial", 10, "bold")).pack(anchor="w")

        Radiobutton(
            sort_frame, text="숫자 기준",
            variable=self.sort_mode, value=1,
            command=self._on_sort_changed
        ).pack(anchor="w")

        Radiobutton(
            sort_frame, text="알파벳",
            variable=self.sort_mode, value=2,
            command=self._on_sort_changed
        ).pack(anchor="w")

        Radiobutton(
            sort_frame, text="생성 날짜",
            variable=self.sort_mode, value=3,
            command=self._on_sort_changed
        ).pack(anchor="w")

        Radiobutton(
            sort_frame, text="확장자",
            variable=self.sort_mode, value=4,
            command=self._on_sort_changed
        ).pack(anchor="w")

        regex_frame = Frame(sort_frame)
        regex_frame.pack(anchor="w")
        Radiobutton(
            regex_frame, text="정규식:",
            variable=self.sort_mode, value=5,
            command=self._on_sort_changed
        ).pack(side="left")
        Entry(regex_frame, textvariable=self.regex_pattern, width=20).pack(side="left", padx=5)
        Button(regex_frame, text="적용", command=self._on_sort_changed).pack(side="left")

    def _create_pattern_input(self):
        """파일명 패턴 입력 섹션 생성"""
        pattern_frame = Frame(self.root, padx=10, pady=5)
        pattern_frame.pack(fill="x")

        Label(pattern_frame, text="파일명 패턴:", font=("Arial", 10, "bold")).pack(anchor="w")
        Entry(pattern_frame, textvariable=self.name_pattern, width=30).pack(anchor="w", pady=2)

        example_text = NameGenerator.get_pattern_examples()
        Label(
            pattern_frame, text=example_text,
            fg="gray", font=("Arial", 8)
        ).pack(anchor="w")

    def _create_preview_table(self):
        """미리보기 테이블 생성"""
        preview_frame = Frame(self.root, padx=10, pady=5)
        preview_frame.pack(fill="both", expand=True)

        Label(preview_frame, text="미리보기:", font=("Arial", 10, "bold")).pack(anchor="w")

        table_frame = Frame(preview_frame)
        table_frame.pack(fill="both", expand=True)

        # 좌측: 파일 목록
        list_frame = Frame(table_frame)
        list_frame.pack(side="left", fill="both", expand=True)

        # 헤더
        header_frame = Frame(list_frame)
        header_frame.pack(fill="x")
        Label(
            header_frame, text="원본 파일명",
            width=30, anchor="w", bg="lightgray"
        ).pack(side="left", fill="x", expand=True)
        Label(
            header_frame, text="→",
            width=3, anchor="center", bg="lightgray"
        ).pack(side="left")
        Label(
            header_frame, text="변경 파일명",
            width=30, anchor="w", bg="lightgray"
        ).pack(side="left", fill="x", expand=True)

        # 리스트박스
        listbox_frame = Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9)
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 우측: 순서 변경 버튼
        button_frame = Frame(table_frame, padx=5)
        button_frame.pack(side="right", fill="y")

        Label(button_frame, text="순서\n변경", font=("Arial", 9, "bold")).pack(pady=5)
        Button(button_frame, text="↑", width=3, command=self._on_move_up).pack(pady=2)
        Button(button_frame, text="↓", width=3, command=self._on_move_down).pack(pady=2)

    def _create_action_buttons(self):
        """하단 액션 버튼 생성"""
        action_frame = Frame(self.root, padx=10, pady=10)
        action_frame.pack(fill="x")

        Button(
            action_frame, text="실행",
            bg="green", fg="white", font=("Arial", 10, "bold"),
            width=15, command=self._on_execute
        ).pack(side="left", padx=5)

        Button(
            action_frame, text="되돌리기",
            bg="orange", fg="white", font=("Arial", 10, "bold"),
            width=15, command=self._on_undo
        ).pack(side="left", padx=5)

        Button(
            action_frame, text="종료",
            bg="red", fg="white", font=("Arial", 10, "bold"),
            width=15, command=self.root.quit
        ).pack(side="right", padx=5)

    # ==================== 이벤트 핸들러 ====================

    def _on_select_folder(self):
        """폴더 선택 이벤트"""
        folder = filedialog.askdirectory(title="이미지 폴더를 선택하세요")
        if not folder:
            return

        self.current_folder = Path(folder)
        self.folder_var.set(str(self.current_folder))
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
        """정렬 규칙 변경 이벤트"""
        if self.file_items:
            self._apply_sort()

    def _apply_sort(self):
        """정렬 적용"""
        if not self.file_items:
            return

        mode = self.sort_mode.get()

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
                pattern = self.regex_pattern.get()
                self.file_items = FileSorter.sort_by_regex(self.file_items, pattern)

            FileSorter.update_order(self.file_items)
            self._update_preview()

        except Exception as e:
            messagebox.showerror("정렬 오류", f"정렬 중 오류가 발생했습니다:\n{str(e)}")

    def _update_preview(self):
        """미리보기 업데이트"""
        self.file_listbox.delete(0, "end")

        pattern = self.name_pattern.get()

        for i, item in enumerate(self.file_items):
            new_name = NameGenerator.generate(i + 1, pattern, item.ext)
            item.new_name = new_name

            display = f"{item.original_name:<35} → {new_name}"
            self.file_listbox.insert("end", display)

    def _on_move_up(self):
        """항목 위로 이동"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        index = selection[0]
        if index == 0:
            return  # 이미 최상단

        # 교환
        self.file_items[index], self.file_items[index - 1] = \
            self.file_items[index - 1], self.file_items[index]

        self._update_preview()
        self.file_listbox.selection_clear(0, "end")
        self.file_listbox.selection_set(index - 1)
        self.file_listbox.see(index - 1)

    def _on_move_down(self):
        """항목 아래로 이동"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        index = selection[0]
        if index >= len(self.file_items) - 1:
            return  # 이미 최하단

        # 교환
        self.file_items[index], self.file_items[index + 1] = \
            self.file_items[index + 1], self.file_items[index]

        self._update_preview()
        self.file_listbox.selection_clear(0, "end")
        self.file_listbox.selection_set(index + 1)
        self.file_listbox.see(index + 1)

    def _on_execute(self):
        """파일명 변경 실행"""
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
        """파일명 변경 되돌리기"""
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
