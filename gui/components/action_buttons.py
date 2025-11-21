"""
Action Buttons Component
액션 버튼 UI 컴포넌트 (단일 책임: 액션 버튼 UI)
"""

from tkinter import Frame, Button
from typing import Optional, Callable
from gui.modern_style import ModernStyle


class ActionButtons(Frame):
    """
    액션 버튼 컴포넌트
    책임: 실행, 되돌리기, 종료 버튼 표시 및 이벤트 처리
    """

    def __init__(self, parent,
                 on_execute: Optional[Callable] = None,
                 on_undo: Optional[Callable] = None,
                 on_quit: Optional[Callable] = None):
        """
        초기화

        Args:
            parent: 부모 위젯
            on_execute: 실행 버튼 클릭 시 호출될 콜백
            on_undo: 되돌리기 버튼 클릭 시 호출될 콜백
            on_quit: 종료 버튼 클릭 시 호출될 콜백
        """
        super().__init__(parent, **ModernStyle.get_frame_style())
        self.on_execute = on_execute
        self.on_undo = on_undo
        self.on_quit = on_quit

        self._create_ui()

    def _create_ui(self):
        """UI 생성"""
        # 컨테이너
        container = Frame(self, **ModernStyle.get_frame_style())
        container.pack(fill="x", padx=ModernStyle.SPACING['xl'],
                      pady=ModernStyle.SPACING['lg'])

        # 좌측: 실행 버튼
        Button(
            container,
            text="실행",
            font=ModernStyle.create_font('body', 'bold'),
            width=18,
            command=lambda: self.on_execute() if self.on_execute else None,
            cursor="hand2",
            **ModernStyle.get_button_style('success')
        ).pack(side="left", padx=(0, ModernStyle.SPACING['sm']))

        # 되돌리기 버튼
        Button(
            container,
            text="되돌리기",
            font=ModernStyle.create_font('body', 'bold'),
            width=18,
            command=lambda: self.on_undo() if self.on_undo else None,
            cursor="hand2",
            **ModernStyle.get_button_style('warning')
        ).pack(side="left", padx=ModernStyle.SPACING['sm'])

        # 우측: 종료 버튼
        Button(
            container,
            text="종료",
            font=ModernStyle.create_font('body', 'bold'),
            width=18,
            command=lambda: self.on_quit() if self.on_quit else None,
            cursor="hand2",
            **ModernStyle.get_button_style('secondary')
        ).pack(side="right")
