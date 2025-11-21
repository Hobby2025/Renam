#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renam - Image File Sorter and Renamer
이미지 파일 정렬 및 일괄 이름 변경 도구

클린코드 원칙:
- 단일 책임 원칙(SRP): 각 모듈은 하나의 책임만 가짐
- 의존성 역전 원칙(DIP): GUI는 core 모듈에 의존
- 개방-폐쇄 원칙(OCP): 새로운 정렬 방식 추가 용이

구조:
- models/: 데이터 모델
- core/: 비즈니스 로직 (정렬, 파일처리, Undo 등)
- gui/: 사용자 인터페이스
"""

import sys
import customtkinter as ctk
from gui.main_window import RenamMainWindow


def main():
    """
    애플리케이션 진입점
    책임: 애플리케이션 초기화 및 실행
    """
    try:
        # CustomTkinter 기본 설정
        ctk.set_appearance_mode("dark")  # "light" or "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        root = ctk.CTk()
        app = RenamMainWindow(root)
        app.run()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
