"""
Name Generator Module
파일명 패턴 생성 로직 (단일 책임: 파일명 생성)
"""

import re
from typing import Set


class NameGenerator:
    """
    파일명 패턴 기반 이름 생성 클래스
    책임: 패턴에 따른 새 파일명 생성
    """

    # 지원하는 이미지 확장자
    IMAGE_EXTENSIONS: Set[str] = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp',
        '.webp', '.tiff', '.tif'
    }

    @staticmethod
    def generate(index: int, pattern: str, extension: str) -> str:
        """
        패턴에 따라 새 파일명 생성

        Args:
            index: 파일 순번 (1부터 시작)
            pattern: 파일명 패턴 (예: {n}, {000}, IMG_{00})
            extension: 파일 확장자 (예: .jpg)

        Returns:
            생성된 파일명

        Examples:
            >>> NameGenerator.generate(1, "{n}", ".jpg")
            "1.jpg"
            >>> NameGenerator.generate(5, "IMG_{000}", ".png")
            "IMG_005.png"
            >>> NameGenerator.generate(10, "{00}", ".jpg")
            "10.jpg"
        """
        result = pattern

        # {000}, {00}, {0} 형태의 제로 패딩 처리
        zero_patterns = re.findall(r'\{(0+)\}', result)
        for zp in zero_patterns:
            width = len(zp)
            result = result.replace(f'{{{zp}}}', str(index).zfill(width))

        # {n} 처리
        result = result.replace('{n}', str(index))

        # 확장자 추가 (확장자가 없으면 원본 확장자 사용)
        if not NameGenerator._has_extension(result):
            result += extension

        return result

    @staticmethod
    def _has_extension(filename: str) -> bool:
        """
        파일명에 확장자가 있는지 확인

        Args:
            filename: 파일명

        Returns:
            확장자 존재 여부
        """
        return any(filename.endswith(ext) for ext in NameGenerator.IMAGE_EXTENSIONS)

    @staticmethod
    def validate_pattern(pattern: str) -> bool:
        """
        패턴 유효성 검증

        Args:
            pattern: 파일명 패턴

        Returns:
            유효성 여부
        """
        # 빈 패턴 체크
        if not pattern or not pattern.strip():
            return False

        # 최소한 {n} 또는 {0...} 패턴이 있어야 함
        has_pattern = bool(re.search(r'\{(n|0+)\}', pattern))
        return has_pattern

    @staticmethod
    def check_duplicates(filenames: list) -> bool:
        """
        중복 파일명 검사

        Args:
            filenames: 파일명 리스트

        Returns:
            중복 존재 여부
        """
        return len(filenames) != len(set(filenames))

    @staticmethod
    def get_pattern_examples() -> str:
        """
        패턴 예시 문자열 반환

        Returns:
            패턴 예시 설명
        """
        return "예시: {n} → 1, 2, 3 | {000} → 001, 002 | IMG_{00} → IMG_01, IMG_02"
