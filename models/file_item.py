"""
File Item Data Model
파일 정보를 담는 데이터 모델 (단일 책임: 데이터 표현)
"""

from pathlib import Path
from typing import Dict


class FileItem:
    """
    파일 정보를 담는 데이터 클래스
    책임: 파일 메타데이터 저장 및 접근
    """

    def __init__(self, filepath: Path):
        """
        파일 아이템 초기화

        Args:
            filepath: 파일 경로 (Path 객체)
        """
        self.original_path = filepath
        self.original_name = filepath.name
        self.display_name = filepath.name
        self.new_name = ""
        self.order = 0
        self.ext = filepath.suffix.lower()
        self.stat = filepath.stat()

    def to_dict(self) -> Dict:
        """
        딕셔너리 형태로 변환 (직렬화용)

        Returns:
            파일 정보 딕셔너리
        """
        return {
            "original": self.original_name,
            "display_name": self.display_name,
            "new_name": self.new_name,
            "order": self.order,
            "ext": self.ext
        }

    def __repr__(self):
        return f"FileItem({self.original_name} → {self.new_name})"

    def __str__(self):
        return f"{self.original_name} → {self.new_name}"
