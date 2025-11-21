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
│   ├── modern_style.py    # 모던 UI 디자인 시스템
│   ├── main_window.py     # GUI 메인 윈도우 (오케스트레이터)
│   └── components/        # 재사용 가능한 UI 컴포넌트
│       ├── __init__.py
│       ├── folder_selector.py   # 상위 폴더 선택 컴포넌트
│       ├── folder_list.py       # 하위 폴더 리스트(탭) 컴포넌트
│       ├── sort_options.py      # 정렬 옵션 컴포넌트
│       ├── pattern_input.py     # 패턴 입력 컴포넌트
│       ├── preview_table.py     # 미리보기 테이블 컴포넌트
│       ├── action_buttons.py    # 액션 버튼 컴포넌트
│       └── tab_manager.py       # (사용 여부에 따라) 탭 스타일 UI 컴포넌트
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

#### `modern_style.py`

- **책임**: UI 디자인 시스템 (색상, 폰트, 스타일)
- **기능**:
  - 모던 미니멀 디자인 색상 팔레트
  - 시스템 폰트 설정 (macOS/Windows)
  - 8pt 그리드 시스템 간격
  - 컴포넌트별 스타일 제공

```python
ModernStyle
  ├── COLORS              # 색상 정의
  ├── FONTS               # 폰트 설정
  ├── FONT_SIZES          # 폰트 크기
  ├── SPACING             # 간격 시스템
  ├── get_button_style()  # 버튼 스타일
  ├── get_frame_style()   # 프레임 스타일
  ├── get_label_style()   # 레이블 스타일
  └── create_font()       # 폰트 객체 생성
```

#### `main_window.py`

- **책임**: UI 컴포넌트 조립 및 이벤트 조정 (오케스트레이터)
- **기능**:
  - 컴포넌트 생성 및 배치 (좌측: 하위 폴더/옵션, 우측: 미리보기, 하단: 실행 버튼)
  - 컴포넌트 간 이벤트 조정
  - core 계층 호출 및 결과 전달
  - 전역 상태 관리 (상위 폴더, 하위 폴더 목록, 현재 탭, 탭별 데이터)

```python
RenamMainWindow
  ├── folder_selector     # FolderSelector 컴포넌트
  ├── folder_list         # FolderList 컴포넌트 (하위 폴더 리스트 & 현재 탭 관리)
  ├── sort_options        # SortOptions 컴포넌트
  ├── pattern_input       # PatternInput 컴포넌트
  ├── preview_table       # PreviewTable 컴포넌트
  ├── action_buttons      # ActionButtons 컴포넌트
  ├── _on_folder_selected()  # 폴더 선택 이벤트 조정
  ├── _scan_subfolders_and_setup_list()  # 하위 폴더 스캔 및 탭 데이터 초기화
  ├── _show_folder()         # 탭(하위 폴더) 전환 및 탭별 상태 복원
  ├── _on_sort_changed()     # 정렬 변경 이벤트 조정
  ├── _apply_sort()          # 현재 정렬 규칙에 따른 정렬 + order 업데이트
  ├── _update_preview()      # 패턴 적용 후 PreviewTable 업데이트 (미리보기 타이틀 포함)
  ├── _rescan_folder()       # 이름 변경/Undo/초기화 후 폴더 재스캔 + 정렬 재적용
  ├── _on_move_up/down()     # 항목 이동 이벤트 조정
  ├── _on_execute_all()      # 하단 실행 버튼 (단일 폴더 / 현재 탭 기준 실행)
  └── _on_undo_all()         # 하단 되돌리기 버튼 (단일 폴더 / 현재 탭 기준 Undo)
```

#### `components/` - 재사용 가능한 UI 컴포넌트

각 컴포넌트는 **단일 책임**을 가지며 **독립적으로 재사용** 가능합니다.

##### `folder_selector.py`

- **책임**: 폴더 선택 UI
- **기능**: 폴더 다이얼로그, 경로 표시, 선택 콜백

##### `sort_options.py`

- **책임**: 정렬 옵션 선택 UI
- **기능**: 라디오 버튼, 정규식 입력, 선택 콜백

##### `pattern_input.py`

- **책임**: 파일명 패턴 입력 UI
- **기능**: 패턴 입력 필드, 예시 표시

##### `preview_table.py`

- **책임**: 파일 목록 미리보기 UI
- **기능**:
  - 헤더 타이틀 (`미리보기` / `미리보기 > {폴더명}`) 표시
  - 원본/변경 파일명 그리드 렌더링
  - 위/아래/제거/초기화 버튼을 통한 순서/목록 조작
  - 선택 상태(다중 선택, Shift/Ctrl) 관리
  - 위젯 재사용으로 대량 리스트 업데이트 시 깜빡임 최소화

##### `folder_list.py`

- **책임**: 하위 폴더 리스트 및 현재 선택된 폴더(탭) 관리
- **기능**:
  - 좌측 `하위 폴더` 영역에서 하위 폴더 목록을 수직 리스트로 표시
  - 행/텍스트 클릭 시 `select_folder` 를 통해 현재 탭 변경
  - 현재 폴더/비선택 폴더 스타일(배경색, 폰트) 구분
  - `set_folders`에서 row 위젯을 재사용하여 리스트 깜빡임 최소화

##### `action_buttons.py`

- **책임**: 액션 버튼 UI
- **기능**: 실행, 되돌리기, 종료 버튼

## 설계 원칙

### 단일 책임 원칙 (SRP)

각 모듈과 클래스는 **하나의 책임**만 가집니다:

**비즈니스 로직**:

- `FileItem`: 파일 데이터 표현
- `FileSorter`: 정렬 로직
- `NameGenerator`: 파일명 생성
- `FileOperations`: 파일 시스템 작업
- `UndoManager`: Undo 관리

**프레젠테이션**:

- `ModernStyle`: UI 디자인 시스템
- `RenamMainWindow`: 컴포넌트 조립 및 이벤트 조정
- `FolderSelector`: 폴더 선택 UI
- `SortOptions`: 정렬 옵션 UI
- `PatternInput`: 패턴 입력 UI
- `PreviewTable`: 미리보기 테이블 UI
- `ActionButtons`: 액션 버튼 UI

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
   - 상위 폴더 선택 (FolderSelector)
   - 하위 폴더 선택 (FolderList → 현재 탭)
   - 정렬 규칙/패턴 변경 (SortOptions, PatternInput)
   - 순서 조정/초기화/실행/되돌리기 (PreviewTable, ActionButtons)
   ↓
2. 이벤트 핸들러 (RenamMainWindow)
   - `_scan_subfolders_and_setup_list` 로 하위 폴더 스캔 + `tab_data` 구성
   - `_show_folder` 로 탭 전환 및 탭별 상태 복원
   - `_apply_sort` 로 현재 정렬 규칙 적용 + `FileSorter.update_order`
   - `_update_preview` 로 패턴 적용 및 PreviewTable 갱신
   - `_rescan_folder` 로 이름 변경/Undo/초기화 이후 재스캔 + 정렬 재적용
   ↓
3. 비즈니스 로직 호출 (FileSorter, NameGenerator, FileOperations)
   ↓
4. 데이터 모델 조작 (FileItem)
   ↓
5. 결과 반환 → GUI 업데이트 (FolderList/PreviewTable/ActionButtons 상태 반영)
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
# gui/components/에 새 컴포넌트 생성
class AdvancedOptions(Frame):
    def __init__(self, parent, on_change=None):
        super().__init__(parent, **ModernStyle.get_frame_style())
        # 고급 옵션 UI 구성

# gui/main_window.py에서 사용
self.advanced_options = AdvancedOptions(content_frame, on_change=self._on_advanced_changed)
self.advanced_options.pack(fill="x")
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

### After (컴포넌트 기반 모듈 분리)

```
app.py (40 lines) - 진입점

models/
  └── file_item.py (50 lines) - 데이터 모델

core/
  ├── sorter.py (120 lines) - 정렬 로직
  ├── name_generator.py (100 lines) - 파일명 생성
  ├── file_operations.py (120 lines) - 파일 작업
  └── undo_manager.py (80 lines) - Undo 관리

gui/
  ├── modern_style.py (260 lines) - 디자인 시스템
  ├── main_window.py (290 lines) - 이벤트 조정
  └── components/
      ├── folder_selector.py (110 lines) - 폴더 선택 UI
      ├── sort_options.py (130 lines) - 정렬 옵션 UI
      ├── pattern_input.py (70 lines) - 패턴 입력 UI
      ├── preview_table.py (160 lines) - 미리보기 UI
      └── action_buttons.py (60 lines) - 액션 버튼 UI
```

**결과**:

- 각 파일이 40~290줄로 관리하기 쉬운 크기
- 각 모듈/컴포넌트의 책임이 명확
- UI 컴포넌트 재사용 가능
- 테스트 및 확장 용이
- 디자인 시스템 일관성 유지
