"""
Undo Manager Module
실행 취소 관리 로직 (단일 책임: Undo 기록 관리)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class UndoManager:
    """
    파일명 변경 작업의 Undo 기능 관리 클래스
    책임: Undo 로그 저장, 로드, 관리
    """

    def __init__(self, log_file: Path = Path("undo_log.json"), max_logs: int = 10):
        """
        UndoManager 초기화

        Args:
            log_file: 로그 파일 경로
            max_logs: 보관할 최대 로그 개수
        """
        self.log_file = log_file
        self.max_logs = max_logs

    def save_operation(self, folder: Path, before: List[str], after: List[str]) -> None:
        """
        파일명 변경 작업 저장

        Args:
            folder: 작업 폴더
            before: 변경 전 파일명 리스트
            after: 변경 후 파일명 리스트
        """
        undo_data = {
            "folder": str(folder),
            "before": before,
            "after": after,
            "timestamp": datetime.now().isoformat()
        }

        logs = self._load_logs()
        logs.append(undo_data)

        # 최대 개수 유지
        logs = logs[-self.max_logs:]

        self._save_logs(logs)

    def get_last_operation(self) -> Optional[Dict]:
        """
        마지막 작업 가져오기

        Returns:
            마지막 작업 데이터 또는 None
        """
        logs = self._load_logs()
        return logs[-1] if logs else None

    def remove_last_operation(self) -> bool:
        """
        마지막 작업 제거

        Returns:
            제거 성공 여부
        """
        logs = self._load_logs()
        if not logs:
            return False

        logs.pop()
        self._save_logs(logs)
        return True

    def get_all_operations(self) -> List[Dict]:
        """
        모든 작업 기록 가져오기

        Returns:
            작업 기록 리스트
        """
        return self._load_logs()

    def has_operations(self) -> bool:
        """
        Undo 가능한 작업이 있는지 확인

        Returns:
            작업 존재 여부
        """
        return len(self._load_logs()) > 0

    def _load_logs(self) -> List[Dict]:
        """
        로그 파일 로드

        Returns:
            로그 데이터 리스트
        """
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_logs(self, logs: List[Dict]) -> None:
        """
        로그 파일 저장

        Args:
            logs: 저장할 로그 데이터 리스트
        """
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"로그 저장 실패: {str(e)}")

    def clear_all(self) -> None:
        """모든 로그 삭제"""
        if self.log_file.exists():
            self.log_file.unlink()
