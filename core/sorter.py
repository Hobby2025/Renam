"""
Sorting Logic Module
파일 정렬 로직 (단일 책임: 정렬 전략 제공)
"""

import re
from typing import List, Callable
from models.file_item import FileItem


class FileSorter:
    """
    파일 정렬 전략을 제공하는 클래스
    책임: 다양한 정렬 알고리즘 제공
    """

    @staticmethod
    def sort_by_numeric(items: List[FileItem]) -> List[FileItem]:
        """
        숫자 기준 정렬

        Args:
            items: 정렬할 파일 아이템 리스트

        Returns:
            정렬된 파일 아이템 리스트
        """
        return sorted(items, key=FileSorter._numeric_key)

    @staticmethod
    def sort_by_alphabetic(items: List[FileItem]) -> List[FileItem]:
        """
        알파벳 기준 정렬

        Args:
            items: 정렬할 파일 아이템 리스트

        Returns:
            정렬된 파일 아이템 리스트
        """
        return sorted(items, key=lambda x: x.original_name.lower())

    @staticmethod
    def sort_by_date(items: List[FileItem]) -> List[FileItem]:
        """
        생성 날짜 기준 정렬

        Args:
            items: 정렬할 파일 아이템 리스트

        Returns:
            정렬된 파일 아이템 리스트
        """
        return sorted(items, key=lambda x: x.stat.st_ctime)

    @staticmethod
    def sort_by_extension(items: List[FileItem]) -> List[FileItem]:
        """
        확장자 기준 정렬 (확장자별 그룹 후 이름순)

        Args:
            items: 정렬할 파일 아이템 리스트

        Returns:
            정렬된 파일 아이템 리스트
        """
        return sorted(items, key=lambda x: (x.ext, x.original_name.lower()))

    @staticmethod
    def sort_by_regex(items: List[FileItem], pattern: str) -> List[FileItem]:
        """
        정규식 패턴 기준 정렬

        Args:
            items: 정렬할 파일 아이템 리스트
            pattern: 정규식 패턴

        Returns:
            정렬된 파일 아이템 리스트

        Raises:
            re.error: 잘못된 정규식 패턴
        """
        return sorted(items, key=lambda x: FileSorter._regex_key(x, pattern))

    @staticmethod
    def _numeric_key(item: FileItem) -> tuple:
        """
        숫자 기준 정렬 키 생성

        Args:
            item: 파일 아이템

        Returns:
            (숫자, 파일명) 튜플
        """
        numbers = re.findall(r'\d+', item.original_name)
        if numbers:
            return (int(numbers[0]), item.original_name)
        return (float('inf'), item.original_name)

    @staticmethod
    def _regex_key(item: FileItem, pattern: str) -> tuple:
        """
        정규식 기반 정렬 키 생성

        Args:
            item: 파일 아이템
            pattern: 정규식 패턴

        Returns:
            (추출값, 파일명) 튜플
        """
        match = re.search(pattern, item.original_name)
        if match:
            key = match.group(1) if match.groups() else match.group(0)
            # 숫자면 int로 변환
            try:
                return (int(key), item.original_name)
            except ValueError:
                return (key, item.original_name)
        return (float('inf'), item.original_name)

    @staticmethod
    def update_order(items: List[FileItem]) -> None:
        """
        정렬된 아이템들의 order 필드 업데이트

        Args:
            items: 파일 아이템 리스트 (in-place 수정)
        """
        for i, item in enumerate(items):
            item.order = i + 1
