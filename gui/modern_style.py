"""
Modern Clean UI Design Theme
모던하고 깔끔한 디자인 테마 정의 (단일 책임: UI 스타일링)
"""

from tkinter import font


class ModernStyle:
    """
    모던 클린 UI 디자인 시스템
    책임: 색상, 폰트, 스타일 상수 제공
    """

    # 색상 팔레트 (모던 미니멀 디자인)
    COLORS = {
        # 기본 색상
        'background': '#F5F5F7',           # 연한 회색 배경
        'surface': '#FFFFFF',              # 흰색 표면
        'surface_secondary': '#F9F9F9',    # 보조 표면

        # 텍스트 색상
        'text_primary': '#1D1D1F',         # 주요 텍스트 (거의 검정)
        'text_secondary': '#6E6E73',       # 보조 텍스트 (회색)
        'text_tertiary': '#86868B',        # 3차 텍스트 (연한 회색)

        # 액센트 색상
        'accent_blue': '#007AFF',          # 시스템 블루
        'accent_green': '#34C759',         # 시스템 그린
        'accent_orange': '#FF9500',        # 시스템 오렌지
        'accent_red': '#FF3B30',           # 시스템 레드

        # 버튼 색상
        'button_primary': '#007AFF',       # 주요 버튼
        'button_primary_hover': '#0051D5', # 호버 상태
        'button_success': '#34C759',       # 성공 버튼
        'button_warning': '#FF9500',       # 경고 버튼
        'button_danger': '#FF3B30',        # 위험 버튼
        'button_secondary': '#E5E5EA',     # 보조 버튼

        # 구분선
        'separator': '#D1D1D6',            # 구분선
        'border': '#E5E5EA',               # 테두리

        # 선택/호버 상태
        'selected': '#007AFF',             # 선택 상태
        'hover': '#F0F0F5',                # 호버 배경
    }

    # 폰트 설정
    FONTS = {
        'system': 'SF Pro Display',        # macOS
        'fallback': 'Segoe UI',            # Windows
        'fallback2': 'Helvetica Neue',     # 대체 폰트
    }

    # 폰트 크기
    FONT_SIZES = {
        'title': 24,        # 큰 제목
        'headline': 18,     # 헤드라인
        'body': 13,         # 본문
        'subhead': 11,      # 부제목
        'caption': 10,      # 캡션
    }

    # 간격 (8pt 그리드 시스템)
    SPACING = {
        'xs': 4,     # 아주 작은 간격
        'sm': 8,     # 작은 간격
        'md': 16,    # 중간 간격
        'lg': 24,    # 큰 간격
        'xl': 32,    # 아주 큰 간격
    }

    # 모서리 반경
    RADIUS = {
        'sm': 6,     # 작은 버튼
        'md': 8,     # 중간 버튼
        'lg': 12,    # 큰 요소
    }

    @staticmethod
    def get_font_family():
        """
        시스템에 맞는 폰트 반환

        Returns:
            폰트 패밀리 이름
        """
        import platform

        system = platform.system()
        if system == 'Darwin':  # macOS
            return ModernStyle.FONTS['system']
        elif system == 'Windows':
            return ModernStyle.FONTS['fallback']
        else:
            return ModernStyle.FONTS['fallback2']

    @staticmethod
    def create_font(size_key='body', weight='normal'):
        """
        폰트 객체 생성

        Args:
            size_key: FONT_SIZES의 키
            weight: 폰트 굵기 ('normal', 'bold')

        Returns:
            tkinter.font.Font 객체
        """
        family = ModernStyle.get_font_family()
        size = ModernStyle.FONT_SIZES.get(size_key, 13)

        return font.Font(family=family, size=size, weight=weight)

    @staticmethod
    def get_button_style(button_type='primary'):
        """
        버튼 스타일 딕셔너리 반환

        Args:
            button_type: 'primary', 'success', 'warning', 'danger', 'secondary'

        Returns:
            스타일 딕셔너리
        """
        styles = {
            'primary': {
                'bg': ModernStyle.COLORS['button_primary'],
                'fg': '#FFFFFF',
                'activebackground': ModernStyle.COLORS['button_primary_hover'],
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'success': {
                'bg': ModernStyle.COLORS['button_success'],
                'fg': '#FFFFFF',
                'activebackground': '#2AB84A',
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'warning': {
                'bg': ModernStyle.COLORS['button_warning'],
                'fg': '#FFFFFF',
                'activebackground': '#E68600',
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'danger': {
                'bg': ModernStyle.COLORS['button_danger'],
                'fg': '#FFFFFF',
                'activebackground': '#E6342A',
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'secondary': {
                'bg': ModernStyle.COLORS['button_secondary'],
                'fg': ModernStyle.COLORS['text_primary'],
                'activebackground': '#D1D1D6',
                'activeforeground': ModernStyle.COLORS['text_primary'],
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
        }

        return styles.get(button_type, styles['primary'])

    @staticmethod
    def get_frame_style():
        """
        프레임 스타일 반환

        Returns:
            스타일 딕셔너리
        """
        return {
            'bg': ModernStyle.COLORS['surface'],
            'relief': 'flat',
            'borderwidth': 0,
        }

    @staticmethod
    def get_label_style(style_type='primary'):
        """
        레이블 스타일 반환

        Args:
            style_type: 'primary', 'secondary', 'tertiary'

        Returns:
            스타일 딕셔너리
        """
        text_colors = {
            'primary': ModernStyle.COLORS['text_primary'],
            'secondary': ModernStyle.COLORS['text_secondary'],
            'tertiary': ModernStyle.COLORS['text_tertiary'],
        }

        return {
            'bg': ModernStyle.COLORS['surface'],
            'fg': text_colors.get(style_type, text_colors['primary']),
            'relief': 'flat',
        }

    @staticmethod
    def get_entry_style():
        """
        입력 필드 스타일 반환

        Returns:
            스타일 딕셔너리
        """
        return {
            'bg': ModernStyle.COLORS['surface'],
            'fg': ModernStyle.COLORS['text_primary'],
            'relief': 'solid',
            'borderwidth': 1,
            'highlightthickness': 1,
            'highlightbackground': ModernStyle.COLORS['border'],
            'highlightcolor': ModernStyle.COLORS['accent_blue'],
        }

    @staticmethod
    def get_listbox_style():
        """
        리스트박스 스타일 반환

        Returns:
            스타일 딕셔너리
        """
        return {
            'bg': ModernStyle.COLORS['surface'],
            'fg': ModernStyle.COLORS['text_primary'],
            'relief': 'flat',
            'borderwidth': 1,
            'highlightthickness': 0,
            'selectbackground': ModernStyle.COLORS['accent_blue'],
            'selectforeground': '#FFFFFF',
            'activestyle': 'none',
        }
