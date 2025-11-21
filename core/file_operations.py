"""
File Operations Module
파일 시스템 작업 로직 (단일 책임: 파일 입출력)
"""

from pathlib import Path
from typing import List, Tuple
from models.file_item import FileItem
from core.name_generator import NameGenerator


class FileOperations:
    """
    파일 시스템 작업 클래스
    책임: 파일 스캔, 읽기, 이름 변경 등 파일 시스템 작업
    """

    @staticmethod
    def scan_folder(folder_path: Path) -> List[FileItem]:
        """
        폴더에서 이미지 파일 스캔

        Args:
            folder_path: 스캔할 폴더 경로

        Returns:
            이미지 파일 아이템 리스트

        Raises:
            FileNotFoundError: 폴더가 존재하지 않음
            PermissionError: 폴더 접근 권한 없음
        """
        if not folder_path.exists():
            raise FileNotFoundError(f"폴더를 찾을 수 없습니다: {folder_path}")

        if not folder_path.is_dir():
            raise NotADirectoryError(f"폴더가 아닙니다: {folder_path}")

        file_items = []
        for filepath in folder_path.iterdir():
            if filepath.is_file() and FileOperations._is_image_file(filepath):
                file_items.append(FileItem(filepath))

        return file_items

    @staticmethod
    def _is_image_file(filepath: Path) -> bool:
        """
        이미지 파일 여부 확인

        Args:
            filepath: 파일 경로

        Returns:
            이미지 파일 여부
        """
        return filepath.suffix.lower() in NameGenerator.IMAGE_EXTENSIONS

    @staticmethod
    def rename_files(folder: Path, items: List[FileItem]) -> Tuple[bool, str]:
        """
        파일명 일괄 변경 (충돌 방지를 위한 2단계 처리)

        Args:
            folder: 대상 폴더
            items: 파일 아이템 리스트

        Returns:
            (성공 여부, 오류 메시지)
        """
        temp_names = []

        try:
            # 1단계: 임시 이름으로 변경 (충돌 방지)
            for i, item in enumerate(items):
                temp_name = f"__renam_temp_{i}__" + item.ext
                temp_path = folder / temp_name
                item.original_path.rename(temp_path)
                temp_names.append(temp_path)

            # 2단계: 실제 이름으로 변경
            for temp_path, item in zip(temp_names, items):
                new_path = folder / item.new_name
                temp_path.rename(new_path)
                # 아이템 정보 업데이트
                item.original_path = new_path
                item.original_name = item.new_name

            return (True, "")

        except PermissionError as e:
            return (False, f"권한 오류: {str(e)}")
        except OSError as e:
            return (False, f"파일 시스템 오류: {str(e)}")
        except Exception as e:
            return (False, f"예상치 못한 오류: {str(e)}")

    @staticmethod
    def restore_files(folder: Path, before_names: List[str],
                     after_names: List[str]) -> Tuple[bool, str]:
        """
        파일명 복구 (Undo)

        Args:
            folder: 대상 폴더
            before_names: 원래 파일명 리스트
            after_names: 현재 파일명 리스트

        Returns:
            (성공 여부, 오류 메시지)
        """
        try:
            for before, after in zip(before_names, after_names):
                after_path = folder / after
                before_path = folder / before

                if after_path.exists():
                    after_path.rename(before_path)

            return (True, "")

        except Exception as e:
            return (False, f"복구 중 오류 발생: {str(e)}")

    @staticmethod
    def validate_folder(folder_path: Path) -> Tuple[bool, str]:
        """
        폴더 유효성 검증

        Args:
            folder_path: 검증할 폴더 경로

        Returns:
            (유효성 여부, 오류 메시지)
        """
        if not folder_path:
            return (False, "폴더가 선택되지 않았습니다.")

        if not folder_path.exists():
            return (False, "폴더가 존재하지 않습니다.")

        if not folder_path.is_dir():
            return (False, "유효한 폴더가 아닙니다.")

        return (True, "")
