"""
Modern Web-Style UI Design Theme
모던 웹 스타일 디자인 테마 정의 (단일 책임: UI 스타일링)
"""

from tkinter import font


class ModernStyle:
    """
    모던 웹 스타일 UI 디자인 시스템
    책임: 색상, 폰트, 스타일 상수 제공
    """

    # 색상 팔레트 (사용자 정의: 그래픽 디자인 테마 - Light Version)
    COLORS = {
        # 기본 배경 (Color 4: #F2F2F2 활용)
        'background': '#F2F2F2',           
        'background_secondary': '#E6E2DE', # 약간 더 짙은 웜 그레이 (혼합색)

        # 카드/표면
        'surface': '#FFFFFF',              # 순백색 카드 (깔끔함)
        'surface_secondary': '#F9F9F9',    # 아주 연한 회색 (보조 영역)
        'surface_hover': '#EFEFEF',        # 호버 표면

        # 텍스트 색상 (Color 1: #0D0D0C 활용 - 가독성)
        'text_button' : '#FFFFFF',          # 버튼용 흰색
        'text_default' : '#0D0D0C',        
        'text_primary': '#0D0D0C',         # 가장 진한 색
        'text_secondary': '#595045',       # Color 2(#736758)보다 약간 진하게 조정
        'text_tertiary': '#8C7E6D',        # Color 3 (은은한 텍스트)
        'text_disabled': '#BFBFBF',        # Color 5

        # 액센트 색상 (Color 3: #8C7E6D 메인)
        'accent_blue': '#8C7E6D',          # 메인 액센트
        'accent_blue_dark': '#736758',     # 진한 액센트
        'accent_blue_light': '#D9D4CE',    # 연한 액센트 (배경용 - 중간값)

        # 상태 색상
        'accent_green': '#8C7E6D',         # 성공 (테마 통일)
        'accent_green_dark': '#736758',
        'accent_green_light': '#E6E2DE',

        'accent_orange': '#A69B8D',        # 경고 (중간 톤)
        'accent_orange_dark': '#736758',
        'accent_orange_light': '#F2F2F2',

        'accent_red': '#8C7E6D',           # 위험 (테마 통일)
        'accent_red_dark': '#5E5449',
        'accent_red_light': '#F2F2F2',

        # 버튼 색상
        'button_primary': '#8C7E6D',       # Color 3 (메인 버튼)
        'button_primary_hover': '#736758', # Color 2 (호버)
        'button_success': '#8C7E6D',
        'button_success_hover': '#736758',
        'button_warning': '#BFBFBF',       # Color 5
        'button_warning_hover': '#A69B8D',
        'button_danger': '#736758',        # Color 2
        'button_danger_hover': '#5E5449',
        'button_secondary': '#FFFFFF',     # 흰색 버튼
        'button_secondary_hover': '#F2F2F2',

        # 테두리 및 기타
        'separator': '#BFBFBF',            # Color 5
        'border': '#BFBFBF',               # Color 5 (은은한 테두리)
        'border_light': '#E6E2DE',         
        'border_focus': '#8C7E6D',         # 포커스
        'input_bg': '#FFFFFF',             # 입력창 흰색
        
        # 선택/호버 상태
        'selected': '#8C7E6D',             
        'selected_bg': '#E6E2DE',          # 선택 배경 (연한 베이지)
        'row_selected': '#E6E2DE',         # 테이블 행 선택 배경
        'hover': '#F2F2F2',                # 호버 배경
        'shadow': '#000000',               # 그림자
    }

    # 폰트 설정
    FONTS = {
        'system': '맑은 고딕',              # Windows 기본
        'fallback': 'Malgun Gothic',       # Windows 영문
        'fallback2': 'Dotum',              # 대체 폰트
    }

    # 폰트 크기
    FONT_SIZES = {
        'title': 21,        # 큰 제목
        'headline': 18,     # 헤드라인
        'body': 16,         # 본문
        'subhead': 14,      # 부제목
        'micro': 11,
        'caption': 12,      # 캡션
    }

    # 간격 (웹 스타일 - 더 넓은 간격, 8pt 그리드)
    SPACING = {
        'xs': 4,      # 아주 작은 간격
        'sm': 6,     # 작은 간격
        'md': 8,     # 중간 간격
        'lg': 10,     # 큰 간격
        'xl': 12,     # 아주 큰 간격
        'xxl': 14,    # 매우 큰 간격
    }

    # 모서리 반경 (웹 스타일 - 더 둥글게)
    RADIUS = {
        'sm': 6,     # 작은 요소
        'md': 8,     # 중간 요소
        'lg': 10,     # 큰 요소
        'xl': 12,     # 매우 큰 요소
    }

    @staticmethod
    def get_font_family():
        """
        시스템에 맞는 폰트 반환

        Returns:
            폰트 패밀리 이름
        """
        # Windows에서 맑은 고딕 사용
        return ModernStyle.FONTS['system']

    @staticmethod
    def create_font(size_key='body', weight='normal'):
        """
        폰트 튜플 생성 (CustomTkinter 호환)

        Args:
            size_key: FONT_SIZES의 키
            weight: 폰트 굵기 ('normal', 'bold')

        Returns:
            폰트 튜플 (family, size, weight) - CustomTkinter용
        """
        family = ModernStyle.get_font_family()
        size = ModernStyle.FONT_SIZES.get(size_key, 12)

        # CustomTkinter는 튜플 형식의 폰트를 요구
        return (family, size, weight)

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
                'activebackground': ModernStyle.COLORS['button_success_hover'],
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'warning': {
                'bg': ModernStyle.COLORS['button_warning'],
                'fg': ModernStyle.COLORS['text_primary'],
                'activebackground': ModernStyle.COLORS['button_warning_hover'],
                'activeforeground': ModernStyle.COLORS['text_primary'],
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['md'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'danger': {
                'bg': ModernStyle.COLORS['button_danger'],
                'fg': '#FFFFFF',
                'activebackground': ModernStyle.COLORS['button_danger_hover'],
                'activeforeground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'padx': ModernStyle.SPACING['sm'],
                'pady': ModernStyle.SPACING['sm'],
            },
            'secondary': {
                'bg': ModernStyle.COLORS['button_secondary'],
                'fg': ModernStyle.COLORS['text_primary'],
                'activebackground': ModernStyle.COLORS['button_secondary_hover'],
                'activeforeground': ModernStyle.COLORS['text_primary'],
                'relief': 'solid',
                'borderwidth': 1,
                'padx': ModernStyle.SPACING['sm'],
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
            'bg': ModernStyle.COLORS['input_bg'],
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
            'borderwidth': 0,
            'highlightthickness': 0,
            'selectbackground': ModernStyle.COLORS['selected_bg'],
            'selectforeground': ModernStyle.COLORS['text_primary'],
            'activestyle': 'none',
            'selectborderwidth': 0,
        }

    @staticmethod
    def get_card_style():
        """
        카드 스타일 반환 (웹 스타일의 카드 컴포넌트)

        Returns:
            스타일 딕셔너리
        """
        return {
            'fg_color': ModernStyle.COLORS['surface'],
            'corner_radius': ModernStyle.RADIUS['md'],
            'border_width': 1,
            'border_color': ModernStyle.COLORS['border'],
        }

    @staticmethod
    def get_breadcrumb_style():
        """
        브레드크럼 스타일 반환

        Returns:
            스타일 딕셔너리
        """
        return {
            'bg_color': ModernStyle.COLORS['surface_secondary'],
            'text_color': ModernStyle.COLORS['text_secondary'],
            'text_color_active': ModernStyle.COLORS['text_primary'],
            'hover_color': ModernStyle.COLORS['surface_hover'],
            'corner_radius': ModernStyle.RADIUS['sm'],
        }

    @staticmethod
    def get_table_style():
        """
        테이블 스타일 반환

        Returns:
            스타일 딕셔너리
        """
        return {
            'header_bg': ModernStyle.COLORS['background_secondary'],
            'header_text': ModernStyle.COLORS['text_secondary'],
            'row_bg': ModernStyle.COLORS['surface'],
            'row_bg_alt': ModernStyle.COLORS['surface_secondary'],
            'row_hover': ModernStyle.COLORS['row_selected'],
            'row_selected': ModernStyle.COLORS['selected_bg'],  # 선택된 행 배경색
            'border_color': ModernStyle.COLORS['border'],
        }
