# Renam 아키텍처 문서

## 클린코드 원칙 적용

이 프로젝트는 **단일 책임 원칙(Single Responsibility Principle, SRP)**을 준수하여 리팩토링되었습니다.

## 프로젝트 구조

```
Renam/
├── app.py                 # 애플리케이션 진입점
├── models/                # 데이터 모델 계층
│   ├── __init__.py
│   └── file_item.py       # FileItem 데이터 클래스
├── core/                  # 비즈니스 로직 계층
│   ├── __init__.py
│   ├── sorter.py          # 파일 정렬 로직
│   ├── name_generator.py  # 파일명 생성 로직
│   ├── file_operations.py # 파일 시스템 작업
│   └── undo_manager.py    # Undo 기능 관리
├── gui/                   # 프레젠테이션 계층
│   ├── __init__.py
│   └── main_window.py     # GUI 메인 윈도우
├── test_logic.py          # 핵심 로직 테스트
└── requirements.txt       # 의존성
```

## 계층별 책임

### 1. 데이터 모델 계층 (models/)

#### `file_item.py`
- **책임**: 파일 메타데이터 저장 및 표현
- **기능**:
  - 파일 경로, 이름, 확장자 정보 저장
  - 딕셔너리 직렬화 지원

```python
FileItem(filepath: Path)
  └── 파일 정보 캡슐화 (원본명, 새이름, 확장자, 순서 등)
```

### 2. 비즈니스 로직 계층 (core/)

#### `sorter.py`
- **책임**: 파일 정렬 알고리즘 제공
- **기능**:
  - 숫자 기준 정렬
  - 알파벳 기준 정렬
  - 생성 날짜 기준 정렬
  - 확장자 기준 정렬
  - 정규식 기반 정렬
  - 정렬 순서 업데이트

```python
FileSorter
  ├── sort_by_numeric()      # 숫자 추출 후 정렬
  ├── sort_by_alphabetic()   # 알파벳 순 정렬
  ├── sort_by_date()         # 파일 생성일 정렬
  ├── sort_by_extension()    # 확장자별 그룹 정렬
  ├── sort_by_regex()        # 정규식 패턴 정렬
  └── update_order()         # order 필드 업데이트
```

#### `name_generator.py`
- **책임**: 패턴 기반 파일명 생성
- **기능**:
  - 패턴 파싱 ({n}, {000}, {00} 등)
  - 제로 패딩 처리
  - 패턴 유효성 검증
  - 중복 파일명 검사

```python
NameGenerator
  ├── generate()           # 패턴으로 새 파일명 생성
  ├── validate_pattern()   # 패턴 유효성 검증
  ├── check_duplicates()   # 중복 검사
  └── get_pattern_examples()  # 패턴 예시 문자열
```

#### `file_operations.py`
- **책임**: 파일 시스템 입출력 작업
- **기능**:
  - 폴더 스캔
  - 이미지 파일 필터링
  - 파일명 일괄 변경 (2단계 안전 처리)
  - 파일명 복구
  - 폴더 유효성 검증

```python
FileOperations
  ├── scan_folder()       # 폴더에서 이미지 파일 스캔
  ├── rename_files()      # 파일명 일괄 변경 (충돌 방지)
  ├── restore_files()     # 파일명 복구 (Undo)
  └── validate_folder()   # 폴더 유효성 검증
```

#### `undo_manager.py`
- **책임**: Undo 기능 관리
- **기능**:
  - 작업 로그 저장 (JSON)
  - 로그 로드 및 조회
  - 최근 N개 작업 유지
  - 작업 복구 지원

```python
UndoManager
  ├── save_operation()        # 작업 로그 저장
  ├── get_last_operation()    # 마지막 작업 조회
  ├── remove_last_operation() # 마지막 작업 제거
  ├── has_operations()        # 작업 존재 여부
  └── clear_all()             # 모든 로그 삭제
```

### 3. 프레젠테이션 계층 (gui/)

#### `main_window.py`
- **책임**: 사용자 인터페이스 표시 및 이벤트 처리
- **기능**:
  - GUI 컴포넌트 생성 및 배치
  - 사용자 이벤트 처리
  - core 계층 호출 및 결과 표시
  - 오류 메시지 표시

```python
RenamMainWindow
  ├── _create_folder_selector()   # 폴더 선택 UI
  ├── _create_sort_options()      # 정렬 옵션 UI
  ├── _create_pattern_input()     # 패턴 입력 UI
  ├── _create_preview_table()     # 미리보기 테이블 UI
  ├── _create_action_buttons()    # 액션 버튼 UI
  ├── _on_select_folder()         # 폴더 선택 이벤트
  ├── _on_sort_changed()          # 정렬 변경 이벤트
  ├── _on_move_up/down()          # 항목 이동 이벤트
  ├── _on_execute()               # 실행 이벤트
  └── _on_undo()                  # 되돌리기 이벤트
```

## 설계 원칙

### 단일 책임 원칙 (SRP)
각 모듈과 클래스는 **하나의 책임**만 가집니다:

- `FileItem`: 파일 데이터 표현
- `FileSorter`: 정렬 로직
- `NameGenerator`: 파일명 생성
- `FileOperations`: 파일 시스템 작업
- `UndoManager`: Undo 관리
- `RenamMainWindow`: UI 표시 및 이벤트 처리

### 의존성 역전 원칙 (DIP)
- GUI 계층은 비즈니스 로직(core)에 의존
- 비즈니스 로직은 데이터 모델(models)에 의존
- 각 계층은 하위 계층에만 의존

```
GUI Layer (gui/)
    ↓ depends on
Core Layer (core/)
    ↓ depends on
Model Layer (models/)
```

### 개방-폐쇄 원칙 (OCP)
- 새로운 정렬 방식 추가 용이: `FileSorter`에 메서드 추가
- 새로운 파일명 패턴 추가 용이: `NameGenerator` 확장
- 기존 코드 수정 최소화

## 데이터 흐름

```
1. 사용자 입력 (GUI)
   ↓
2. 이벤트 핸들러 (RenamMainWindow)
   ↓
3. 비즈니스 로직 호출 (FileSorter, NameGenerator, FileOperations)
   ↓
4. 데이터 모델 조작 (FileItem)
   ↓
5. 결과 반환 → GUI 업데이트
```

## 테스트 전략

- **단위 테스트**: 각 모듈별 독립 테스트 (`test_logic.py`)
- **통합 테스트**: 전체 워크플로우 테스트
- **커버리지**: 모든 핵심 기능 테스트 완료

## 확장성

### 새로운 정렬 방식 추가
```python
# core/sorter.py에 메서드 추가
@staticmethod
def sort_by_size(items: List[FileItem]) -> List[FileItem]:
    return sorted(items, key=lambda x: x.stat.st_size)
```

### 새로운 파일명 패턴 추가
```python
# core/name_generator.py의 generate() 메서드 확장
# 예: {date}, {YYYY-MM-DD} 등 추가
```

### 새로운 UI 컴포넌트 추가
```python
# gui/main_window.py에 메서드 추가
def _create_advanced_options(self):
    # 고급 옵션 UI 구성
    pass
```

## 장점

1. **유지보수성**: 각 모듈의 책임이 명확하여 수정 범위 최소화
2. **테스트 용이성**: 각 모듈을 독립적으로 테스트 가능
3. **재사용성**: core 계층은 CLI, 웹 등 다른 UI에서도 재사용 가능
4. **확장성**: 새로운 기능 추가 시 기존 코드 영향 최소화
5. **가독성**: 모듈 이름만으로 역할 파악 가능

## 리팩토링 전후 비교

### Before (단일 파일)
```
app.py (600+ lines)
  ├── FileItem 클래스
  ├── RenamApp 클래스
  │   ├── UI 코드
  │   ├── 정렬 로직
  │   ├── 파일 처리 로직
  │   ├── Undo 로직
  │   └── 이벤트 핸들러
  └── main()
```

### After (모듈 분리)
```
app.py (40 lines) - 진입점
models/file_item.py (50 lines) - 데이터
core/sorter.py (120 lines) - 정렬
core/name_generator.py (100 lines) - 파일명 생성
core/file_operations.py (120 lines) - 파일 작업
core/undo_manager.py (80 lines) - Undo
gui/main_window.py (350 lines) - GUI
```

**결과**:
- 각 파일이 100~350줄로 관리하기 쉬운 크기
- 각 모듈의 책임이 명확
- 테스트 및 확장 용이
