#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renam 핵심 로직 테스트 스크립트
GUI 없이 파일 정렬 및 이름 변경 로직을 검증
"""

import re
from pathlib import Path
from typing import List


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

    def __repr__(self):
        return f"FileItem({self.original_name} → {self.new_name})"


def sort_key_numeric(item: FileItem) -> tuple:
    """숫자 기준 정렬 키"""
    numbers = re.findall(r'\d+', item.original_name)
    if numbers:
        return (int(numbers[0]), item.original_name)
    return (float('inf'), item.original_name)


def sort_key_regex(item: FileItem, pattern: str) -> tuple:
    """정규식 기반 정렬 키"""
    match = re.search(pattern, item.original_name)
    if match:
        key = match.group(1) if match.groups() else match.group(0)
        try:
            return (int(key), item.original_name)
        except ValueError:
            return (key, item.original_name)
    return (float('inf'), item.original_name)


def generate_new_name(index: int, pattern: str, ext: str) -> str:
    """패턴에 따라 새 파일명 생성"""
    result = pattern

    # {000}, {00}, {0} 형태의 제로 패딩 처리
    zero_patterns = re.findall(r'\{(0+)\}', result)
    for zp in zero_patterns:
        width = len(zp)
        result = result.replace(f'{{{zp}}}', str(index).zfill(width))

    # {n} 처리
    result = result.replace('{n}', str(index))

    # 확장자 추가
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    if not any(result.endswith(e) for e in IMAGE_EXTENSIONS):
        result += ext

    return result


def test_sorting():
    """정렬 로직 테스트"""
    print("=" * 60)
    print("정렬 로직 테스트")
    print("=" * 60)

    test_dir = Path("test_images")
    if not test_dir.exists():
        print("❌ test_images 디렉토리가 없습니다.")
        return

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    file_items: List[FileItem] = []

    for filepath in test_dir.iterdir():
        if filepath.is_file() and filepath.suffix.lower() in IMAGE_EXTENSIONS:
            file_items.append(FileItem(filepath))

    print(f"\n✅ 총 {len(file_items)}개의 이미지 파일 발견\n")

    # 1. 숫자 기준 정렬 테스트
    print("1️⃣ 숫자 기준 정렬:")
    sorted_items = sorted(file_items, key=sort_key_numeric)
    for i, item in enumerate(sorted_items, 1):
        print(f"   {i}. {item.original_name}")

    # 2. 알파벳 정렬 테스트
    print("\n2️⃣ 알파벳 정렬:")
    sorted_items = sorted(file_items, key=lambda x: x.original_name.lower())
    for i, item in enumerate(sorted_items, 1):
        print(f"   {i}. {item.original_name}")

    # 3. 확장자 정렬 테스트
    print("\n3️⃣ 확장자 정렬:")
    sorted_items = sorted(file_items, key=lambda x: (x.ext, x.original_name.lower()))
    for i, item in enumerate(sorted_items, 1):
        print(f"   {i}. {item.original_name} ({item.ext})")

    # 4. 정규식 정렬 테스트
    print("\n4️⃣ 정규식 정렬 (패턴: r'(\\d+)'):")
    sorted_items = sorted(file_items, key=lambda x: sort_key_regex(x, r'(\d+)'))
    for i, item in enumerate(sorted_items, 1):
        print(f"   {i}. {item.original_name}")


def test_pattern_generation():
    """파일명 패턴 생성 테스트"""
    print("\n" + "=" * 60)
    print("파일명 패턴 생성 테스트")
    print("=" * 60)

    test_cases = [
        ("{n}", ".jpg"),
        ("{000}", ".png"),
        ("{00}", ".jpg"),
        ("IMG_{000}", ".jpg"),
        ("Photo_{n}", ".png"),
        ("image_{00}.jpg", ".png"),  # 확장자가 이미 있는 경우
    ]

    for pattern, ext in test_cases:
        print(f"\n패턴: '{pattern}', 확장자: '{ext}'")
        for i in range(1, 6):
            new_name = generate_new_name(i, pattern, ext)
            print(f"   {i} → {new_name}")


def test_name_collision_detection():
    """파일명 중복 감지 테스트"""
    print("\n" + "=" * 60)
    print("파일명 중복 감지 테스트")
    print("=" * 60)

    test_dir = Path("test_images")
    if not test_dir.exists():
        print("❌ test_images 디렉토리가 없습니다.")
        return

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    file_items: List[FileItem] = []

    for filepath in test_dir.iterdir():
        if filepath.is_file() and filepath.suffix.lower() in IMAGE_EXTENSIONS:
            file_items.append(FileItem(filepath))

    # 정렬
    file_items.sort(key=sort_key_numeric)

    # 패턴 적용
    pattern = "{n}"
    for i, item in enumerate(file_items, 1):
        item.new_name = generate_new_name(i, pattern, item.ext)

    # 중복 체크
    new_names = [item.new_name for item in file_items]
    unique_names = set(new_names)

    print(f"\n총 파일 수: {len(new_names)}")
    print(f"고유 파일명 수: {len(unique_names)}")

    if len(new_names) == len(unique_names):
        print("✅ 중복 파일명 없음")
    else:
        print("❌ 중복 파일명 발견!")
        from collections import Counter
        duplicates = [name for name, count in Counter(new_names).items() if count > 1]
        print(f"중복된 파일명: {duplicates}")

    print("\n변경 예정 파일명:")
    for item in file_items:
        print(f"   {item.original_name:<25} → {item.new_name}")


def main():
    """메인 테스트 실행"""
    print("\n🧪 Renam 핵심 로직 테스트 시작\n")

    test_sorting()
    test_pattern_generation()
    test_name_collision_detection()

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
