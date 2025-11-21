#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renam 핵심 로직 테스트 스크립트 (리팩토링 버전)
클린코드 원칙 적용 후 모듈별 테스트
"""

from pathlib import Path
from typing import List

from models.file_item import FileItem
from core.sorter import FileSorter
from core.name_generator import NameGenerator
from core.file_operations import FileOperations
from core.undo_manager import UndoManager


def test_file_operations():
    """파일 작업 모듈 테스트"""
    print("=" * 60)
    print("📂 FileOperations 모듈 테스트")
    print("=" * 60)

    test_dir = Path("test_images")
    if not test_dir.exists():
        print("❌ test_images 디렉토리가 없습니다.")
        return

    # 폴더 검증
    is_valid, msg = FileOperations.validate_folder(test_dir)
    print(f"\n폴더 검증: {'✅ 성공' if is_valid else '❌ 실패'}")

    # 파일 스캔
    try:
        file_items = FileOperations.scan_folder(test_dir)
        print(f"스캔 결과: ✅ {len(file_items)}개의 이미지 파일 발견")
    except Exception as e:
        print(f"스캔 오류: ❌ {e}")
        return

    return file_items


def test_sorter(file_items: List[FileItem]):
    """정렬 모듈 테스트"""
    print("\n" + "=" * 60)
    print("🔄 FileSorter 모듈 테스트")
    print("=" * 60)

    # 1. 숫자 정렬
    print("\n1️⃣ 숫자 기준 정렬:")
    sorted_items = FileSorter.sort_by_numeric(file_items)
    for i, item in enumerate(sorted_items[:5], 1):
        print(f"   {i}. {item.original_name}")

    # 2. 알파벳 정렬
    print("\n2️⃣ 알파벳 정렬:")
    sorted_items = FileSorter.sort_by_alphabetic(file_items)
    for i, item in enumerate(sorted_items[:5], 1):
        print(f"   {i}. {item.original_name}")

    # 3. 날짜 정렬
    print("\n3️⃣ 생성 날짜 정렬:")
    sorted_items = FileSorter.sort_by_date(file_items)
    for i, item in enumerate(sorted_items[:5], 1):
        print(f"   {i}. {item.original_name}")

    # 4. 확장자 정렬
    print("\n4️⃣ 확장자 정렬:")
    sorted_items = FileSorter.sort_by_extension(file_items)
    for i, item in enumerate(sorted_items[:5], 1):
        print(f"   {i}. {item.original_name} ({item.ext})")

    # 5. 정규식 정렬
    print("\n5️⃣ 정규식 정렬 (패턴: r'(\\d+)'):")
    try:
        sorted_items = FileSorter.sort_by_regex(file_items, r'(\d+)')
        for i, item in enumerate(sorted_items[:5], 1):
            print(f"   {i}. {item.original_name}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")

    # order 업데이트 테스트
    FileSorter.update_order(sorted_items)
    print(f"\n✅ order 필드 업데이트 완료 (1 ~ {len(sorted_items)})")


def test_name_generator():
    """파일명 생성 모듈 테스트"""
    print("\n" + "=" * 60)
    print("📝 NameGenerator 모듈 테스트")
    print("=" * 60)

    test_cases = [
        ("{n}", ".jpg"),
        ("{000}", ".png"),
        ("{00}", ".jpg"),
        ("IMG_{000}", ".jpg"),
        ("Photo_{n}", ".png"),
    ]

    for pattern, ext in test_cases:
        print(f"\n패턴: '{pattern}', 확장자: '{ext}'")
        for i in range(1, 4):
            new_name = NameGenerator.generate(i, pattern, ext)
            print(f"   {i} → {new_name}")

    # 패턴 검증 테스트
    print("\n패턴 유효성 검증:")
    valid_patterns = ["{n}", "{000}", "IMG_{00}"]
    invalid_patterns = ["", "   ", "nopattern"]

    for p in valid_patterns:
        is_valid = NameGenerator.validate_pattern(p)
        print(f"   '{p}': {'✅ 유효' if is_valid else '❌ 무효'}")

    for p in invalid_patterns:
        is_valid = NameGenerator.validate_pattern(p)
        print(f"   '{p}': {'✅ 유효' if is_valid else '❌ 무효'}")

    # 중복 검사 테스트
    print("\n중복 파일명 검사:")
    no_dup = ["1.jpg", "2.jpg", "3.jpg"]
    has_dup = ["1.jpg", "2.jpg", "1.jpg"]

    print(f"   {no_dup}: {'❌ 중복 있음' if NameGenerator.check_duplicates(no_dup) else '✅ 중복 없음'}")
    print(f"   {has_dup}: {'❌ 중복 있음' if NameGenerator.check_duplicates(has_dup) else '✅ 중복 없음'}")


def test_undo_manager():
    """Undo 관리 모듈 테스트"""
    print("\n" + "=" * 60)
    print("↩️  UndoManager 모듈 테스트")
    print("=" * 60)

    test_log = Path("test_undo_log.json")
    manager = UndoManager(log_file=test_log, max_logs=3)

    # 로그 저장
    print("\n로그 저장 테스트:")
    manager.save_operation(
        Path("/test/folder1"),
        ["a.jpg", "b.jpg"],
        ["1.jpg", "2.jpg"]
    )
    print("   ✅ 작업 1 저장")

    manager.save_operation(
        Path("/test/folder2"),
        ["c.jpg", "d.jpg"],
        ["3.jpg", "4.jpg"]
    )
    print("   ✅ 작업 2 저장")

    # 로그 조회
    print("\n로그 조회 테스트:")
    all_ops = manager.get_all_operations()
    print(f"   총 {len(all_ops)}개의 작업 기록")

    has_ops = manager.has_operations()
    print(f"   Undo 가능 여부: {'✅ 가능' if has_ops else '❌ 불가능'}")

    last_op = manager.get_last_operation()
    if last_op:
        print(f"   마지막 작업 폴더: {last_op['folder']}")

    # 로그 제거
    print("\n로그 제거 테스트:")
    removed = manager.remove_last_operation()
    print(f"   제거 결과: {'✅ 성공' if removed else '❌ 실패'}")

    # 정리
    manager.clear_all()
    print("   ✅ 테스트 로그 삭제 완료")


def test_integration(file_items: List[FileItem]):
    """통합 테스트 (전체 워크플로우)"""
    print("\n" + "=" * 60)
    print("🔗 통합 테스트 (전체 워크플로우)")
    print("=" * 60)

    if not file_items:
        print("❌ 파일이 없어 통합 테스트를 건너뜁니다.")
        return

    # 1. 정렬
    print("\n1단계: 숫자 정렬")
    sorted_items = FileSorter.sort_by_numeric(file_items)
    FileSorter.update_order(sorted_items)
    print(f"   ✅ {len(sorted_items)}개 파일 정렬 완료")

    # 2. 파일명 생성
    print("\n2단계: 새 파일명 생성 (패턴: IMG_{000})")
    pattern = "IMG_{000}"
    for i, item in enumerate(sorted_items, 1):
        item.new_name = NameGenerator.generate(i, pattern, item.ext)

    print("   미리보기 (상위 5개):")
    for item in sorted_items[:5]:
        print(f"      {item.original_name:<25} → {item.new_name}")

    # 3. 중복 체크
    print("\n3단계: 중복 파일명 검사")
    new_names = [item.new_name for item in sorted_items]
    has_dup = NameGenerator.check_duplicates(new_names)
    print(f"   {'❌ 중복 발견!' if has_dup else '✅ 중복 없음'}")

    print("\n✅ 전체 워크플로우 테스트 완료!")


def main():
    """메인 테스트 실행"""
    print("\n🧪 Renam 핵심 로직 테스트 (리팩토링 버전)\n")
    print("클린코드 원칙 적용 - 단일 책임 원칙(SRP)\n")

    # 각 모듈별 테스트
    file_items = test_file_operations()

    if file_items:
        test_sorter(file_items)
        test_integration(file_items)

    test_name_generator()
    test_undo_manager()

    print("\n" + "=" * 60)
    print("✅ 모든 모듈 테스트 완료!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
