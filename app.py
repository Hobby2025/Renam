#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renam - Image File Sorter and Renamer
이미지 파일 정렬 및 일괄 이름 변경 도구
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, Frame, Listbox, Scrollbar, StringVar, IntVar, Radiobutton, messagebox, filedialog
from tkinter import ttk
from typing import List, Dict, Optional, Callable


class FileItem:
    """파일 정보를 담는 데이터 클래스"""
    def __init__(self, filepath: Path):
        self.original_path = filepath
        self.original_name = filepath.name
        self.display_name = filepath.name
        self.new_name = ""
        self.order = 0
        self.ext = filepath.suffix.lower()
        self.stat = filepath.stat()

    def to_dict(self) -> Dict:
        return {
            "original": self.original_name,
            "display_name": self.display_name,
            "new_name": self.new_name,
            "order": self.order,
            "ext": self.ext
        }


class RenamApp:
    """Renam 메인 애플리케이션 클래스"""

    # 지원하는 이미지 확장자
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}

    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Renam 📁✨")
        self.root.geometry("900x700")

        # 데이터 저장
        self.current_folder: Optional[Path] = None
        self.file_items: List[FileItem] = []
        self.undo_log_path = Path("undo_log.json")

        # GUI 변수
        self.folder_var = StringVar(value="폴더를 선택하세요")
        self.sort_mode = IntVar(value=1)  # 1: 숫자, 2: 알파벳, 3: 날짜, 4: 확장자, 5: 정규식
        self.regex_pattern = StringVar(value=r"(\d+)")
        self.name_pattern = StringVar(value="{n}")

        self.setup_ui()

    def setup_ui(self):
        """UI 구성"""
        # 폴더 선택 섹션
        folder_frame = Frame(self.root, padx=10, pady=10)
        folder_frame.pack(fill="x")

        Label(folder_frame, text="📂 폴더 선택:", font=("Arial", 10)).pack(side="left")
        Label(folder_frame, textvariable=self.folder_var, relief="sunken", width=50).pack(side="left", padx=5)
        Button(folder_frame, text="찾아보기", command=self.select_folder).pack(side="left")

        # 정렬 규칙 섹션
        sort_frame = Frame(self.root, padx=10, pady=5)
        sort_frame.pack(fill="x")

        Label(sort_frame, text="정렬 규칙:", font=("Arial", 10, "bold")).pack(anchor="w")

        Radiobutton(sort_frame, text="숫자 기준", variable=self.sort_mode, value=1,
                   command=self.on_sort_changed).pack(anchor="w")
        Radiobutton(sort_frame, text="알파벳", variable=self.sort_mode, value=2,
                   command=self.on_sort_changed).pack(anchor="w")
        Radiobutton(sort_frame, text="생성 날짜", variable=self.sort_mode, value=3,
                   command=self.on_sort_changed).pack(anchor="w")
        Radiobutton(sort_frame, text="확장자", variable=self.sort_mode, value=4,
                   command=self.on_sort_changed).pack(anchor="w")

        regex_frame = Frame(sort_frame)
        regex_frame.pack(anchor="w")
        Radiobutton(regex_frame, text="정규식:", variable=self.sort_mode, value=5,
                   command=self.on_sort_changed).pack(side="left")
        Entry(regex_frame, textvariable=self.regex_pattern, width=20).pack(side="left", padx=5)
        Button(regex_frame, text="적용", command=self.on_sort_changed).pack(side="left")

        # 파일명 패턴 섹션
        pattern_frame = Frame(self.root, padx=10, pady=5)
        pattern_frame.pack(fill="x")

        Label(pattern_frame, text="파일명 패턴:", font=("Arial", 10, "bold")).pack(anchor="w")
        Entry(pattern_frame, textvariable=self.name_pattern, width=30).pack(anchor="w", pady=2)
        Label(pattern_frame, text="예시: {n} → 1, 2, 3 | {000} → 001, 002 | IMG_{00} → IMG_01, IMG_02",
              fg="gray", font=("Arial", 8)).pack(anchor="w")

        # 미리보기 섹션
        preview_frame = Frame(self.root, padx=10, pady=5)
        preview_frame.pack(fill="both", expand=True)

        Label(preview_frame, text="미리보기:", font=("Arial", 10, "bold")).pack(anchor="w")

        # 테이블 헤더와 리스트박스
        table_frame = Frame(preview_frame)
        table_frame.pack(fill="both", expand=True)

        # 좌측: 파일 목록
        list_frame = Frame(table_frame)
        list_frame.pack(side="left", fill="both", expand=True)

        # 헤더
        header_frame = Frame(list_frame)
        header_frame.pack(fill="x")
        Label(header_frame, text="원본 파일명", width=30, anchor="w", bg="lightgray").pack(side="left", fill="x", expand=True)
        Label(header_frame, text="→", width=3, anchor="center", bg="lightgray").pack(side="left")
        Label(header_frame, text="변경 파일명", width=30, anchor="w", bg="lightgray").pack(side="left", fill="x", expand=True)

        # 리스트박스와 스크롤바
        listbox_frame = Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # 우측: 이동 버튼
        button_frame = Frame(table_frame, padx=5)
        button_frame.pack(side="right", fill="y")

        Label(button_frame, text="순서\n변경", font=("Arial", 9, "bold")).pack(pady=5)
        Button(button_frame, text="↑", width=3, command=self.move_up).pack(pady=2)
        Button(button_frame, text="↓", width=3, command=self.move_down).pack(pady=2)

        # 하단 버튼
        action_frame = Frame(self.root, padx=10, pady=10)
        action_frame.pack(fill="x")

        Button(action_frame, text="실행", bg="green", fg="white", font=("Arial", 10, "bold"),
               width=15, command=self.execute_rename).pack(side="left", padx=5)
        Button(action_frame, text="되돌리기", bg="orange", fg="white", font=("Arial", 10, "bold"),
               width=15, command=self.undo_rename).pack(side="left", padx=5)
        Button(action_frame, text="종료", bg="red", fg="white", font=("Arial", 10, "bold"),
               width=15, command=self.root.quit).pack(side="right", padx=5)

    def select_folder(self):
        """폴더 선택 다이얼로그"""
        folder = filedialog.askdirectory(title="이미지 폴더를 선택하세요")
        if folder:
            self.current_folder = Path(folder)
            self.folder_var.set(str(self.current_folder))
            self.scan_files()

    def scan_files(self):
        """폴더에서 이미지 파일 스캔"""
        if not self.current_folder or not self.current_folder.exists():
            messagebox.showerror("오류", "유효한 폴더를 선택하세요.")
            return

        # 이미지 파일만 필터링
        self.file_items = []
        for filepath in self.current_folder.iterdir():
            if filepath.is_file() and filepath.suffix.lower() in self.IMAGE_EXTENSIONS:
                self.file_items.append(FileItem(filepath))

        if not self.file_items:
            messagebox.showwarning("경고", "선택한 폴더에 이미지 파일이 없습니다.")
            return

        # 초기 정렬 적용
        self.apply_sort()
        messagebox.showinfo("완료", f"{len(self.file_items)}개의 이미지 파일을 찾았습니다.")

    def apply_sort(self):
        """현재 선택된 정렬 규칙 적용"""
        if not self.file_items:
            return

        mode = self.sort_mode.get()

        try:
            if mode == 1:  # 숫자 기준
                self.file_items.sort(key=self._sort_key_numeric)
            elif mode == 2:  # 알파벳
                self.file_items.sort(key=lambda x: x.original_name.lower())
            elif mode == 3:  # 생성 날짜
                self.file_items.sort(key=lambda x: x.stat.st_ctime)
            elif mode == 4:  # 확장자
                self.file_items.sort(key=lambda x: (x.ext, x.original_name.lower()))
            elif mode == 5:  # 정규식
                pattern = self.regex_pattern.get()
                self.file_items.sort(key=lambda x: self._sort_key_regex(x, pattern))
        except Exception as e:
            messagebox.showerror("정렬 오류", f"정렬 중 오류가 발생했습니다:\n{str(e)}")
            return

        # order 업데이트
        for i, item in enumerate(self.file_items):
            item.order = i + 1

        self.update_preview()

    def _sort_key_numeric(self, item: FileItem) -> tuple:
        """숫자 기준 정렬 키"""
        # 파일명에서 숫자 추출
        numbers = re.findall(r'\d+', item.original_name)
        if numbers:
            return (int(numbers[0]), item.original_name)
        return (float('inf'), item.original_name)

    def _sort_key_regex(self, item: FileItem, pattern: str) -> tuple:
        """정규식 기반 정렬 키"""
        match = re.search(pattern, item.original_name)
        if match:
            key = match.group(1) if match.groups() else match.group(0)
            # 숫자면 int로 변환
            try:
                return (int(key), item.original_name)
            except ValueError:
                return (key, item.original_name)
        return (float('inf'), item.original_name)

    def update_preview(self):
        """미리보기 업데이트"""
        self.file_listbox.delete(0, "end")

        pattern = self.name_pattern.get()

        for i, item in enumerate(self.file_items):
            # 새 파일명 생성
            new_name = self.generate_new_name(i + 1, pattern, item.ext)
            item.new_name = new_name

            # 리스트박스에 표시
            display = f"{item.original_name:<35} → {new_name}"
            self.file_listbox.insert("end", display)

    def generate_new_name(self, index: int, pattern: str, ext: str) -> str:
        """패턴에 따라 새 파일명 생성"""
        # {n} → 숫자
        result = pattern

        # {000}, {00}, {0} 형태의 제로 패딩 처리
        zero_patterns = re.findall(r'\{(0+)\}', result)
        for zp in zero_patterns:
            width = len(zp)
            result = result.replace(f'{{{zp}}}', str(index).zfill(width))

        # {n} 처리
        result = result.replace('{n}', str(index))

        # 확장자 추가 (확장자가 없으면 원본 확장자 사용)
        if not any(result.endswith(e) for e in self.IMAGE_EXTENSIONS):
            result += ext

        return result

    def on_sort_changed(self):
        """정렬 규칙 변경 시 호출"""
        if self.file_items:
            self.apply_sort()

    def move_up(self):
        """선택된 항목을 위로 이동"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        index = selection[0]
        if index == 0:
            return  # 이미 최상단

        # 리스트 교환
        self.file_items[index], self.file_items[index - 1] = \
            self.file_items[index - 1], self.file_items[index]

        self.update_preview()
        self.file_listbox.selection_clear(0, "end")
        self.file_listbox.selection_set(index - 1)
        self.file_listbox.see(index - 1)

    def move_down(self):
        """선택된 항목을 아래로 이동"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showinfo("알림", "이동할 항목을 선택하세요.")
            return

        index = selection[0]
        if index >= len(self.file_items) - 1:
            return  # 이미 최하단

        # 리스트 교환
        self.file_items[index], self.file_items[index + 1] = \
            self.file_items[index + 1], self.file_items[index]

        self.update_preview()
        self.file_listbox.selection_clear(0, "end")
        self.file_listbox.selection_set(index + 1)
        self.file_listbox.see(index + 1)

    def execute_rename(self):
        """파일명 변경 실행"""
        if not self.file_items:
            messagebox.showwarning("경고", "파일이 없습니다.")
            return

        # 확인 다이얼로그
        result = messagebox.askyesno("확인",
            f"{len(self.file_items)}개의 파일명을 변경하시겠습니까?\n이 작업은 실제 파일명을 변경합니다.")

        if not result:
            return

        # Undo 로그 준비
        undo_data = {
            "folder": str(self.current_folder),
            "before": [],
            "after": [],
            "timestamp": datetime.now().isoformat()
        }

        # 중복 파일명 체크
        new_names = [item.new_name for item in self.file_items]
        if len(new_names) != len(set(new_names)):
            messagebox.showerror("오류", "중복된 파일명이 발생합니다. 패턴을 수정하세요.")
            return

        # 임시 이름으로 먼저 변경 (충돌 방지)
        temp_names = []
        try:
            for i, item in enumerate(self.file_items):
                temp_name = f"__renam_temp_{i}__" + item.ext
                temp_path = self.current_folder / temp_name
                item.original_path.rename(temp_path)
                temp_names.append(temp_path)
                undo_data["before"].append(item.original_name)

            # 실제 이름으로 변경
            for temp_path, item in zip(temp_names, self.file_items):
                new_path = self.current_folder / item.new_name
                temp_path.rename(new_path)
                item.original_path = new_path
                item.original_name = item.new_name
                undo_data["after"].append(item.new_name)

            # Undo 로그 저장
            self.save_undo_log(undo_data)

            messagebox.showinfo("완료", f"{len(self.file_items)}개의 파일명이 변경되었습니다.")

            # 재스캔
            self.scan_files()

        except Exception as e:
            messagebox.showerror("오류", f"파일명 변경 중 오류가 발생했습니다:\n{str(e)}")

    def save_undo_log(self, undo_data: Dict):
        """Undo 로그를 JSON 파일로 저장"""
        logs = []

        # 기존 로그 읽기
        if self.undo_log_path.exists():
            try:
                with open(self.undo_log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        # 새 로그 추가
        logs.append(undo_data)

        # 최근 10개만 유지
        logs = logs[-10:]

        # 저장
        with open(self.undo_log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def undo_rename(self):
        """마지막 파일명 변경 되돌리기"""
        if not self.undo_log_path.exists():
            messagebox.showinfo("알림", "되돌릴 작업이 없습니다.")
            return

        try:
            with open(self.undo_log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)

            if not logs:
                messagebox.showinfo("알림", "되돌릴 작업이 없습니다.")
                return

            # 마지막 로그 가져오기
            last_log = logs[-1]
            folder = Path(last_log["folder"])

            if not folder.exists():
                messagebox.showerror("오류", "원본 폴더를 찾을 수 없습니다.")
                return

            # 확인
            result = messagebox.askyesno("확인",
                f"마지막 작업을 되돌리시겠습니까?\n폴더: {folder}\n시간: {last_log['timestamp']}")

            if not result:
                return

            # 되돌리기 실행
            for before, after in zip(last_log["before"], last_log["after"]):
                after_path = folder / after
                before_path = folder / before

                if after_path.exists():
                    after_path.rename(before_path)

            # 로그에서 제거
            logs.pop()
            with open(self.undo_log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("완료", "파일명이 복구되었습니다.")

            # 현재 폴더가 동일하면 재스캔
            if self.current_folder == folder:
                self.scan_files()

        except Exception as e:
            messagebox.showerror("오류", f"되돌리기 중 오류가 발생했습니다:\n{str(e)}")


def main():
    """메인 함수"""
    root = Tk()
    app = RenamApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
