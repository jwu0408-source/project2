# 프론트엔드 안내

## 개요
HTML + CSS + Vanilla JavaScript SPA. **Backend의 `contact_app/static/index.html`에 통합되어 있습니다.**
Backend 포트(8000)에서만 접속하세요. 별도 Frontend 서버 불필요합니다.

## 기술 스택
- HTML5, CSS3, Vanilla JavaScript (ES6+)
- Fetch API (절대 경로)
- 세션 쿠키 (HttpOnly, 자동 관리)

## 프로젝트 구조
```
contact_app/static/
└── index.html    # 전체 Frontend (HTML+CSS+JS 통합)
```

## 실행 방법

### 1. PostgreSQL 컨테이너 확인
```bash
# contact_postgres 실행 상태 확인
docker ps | grep contact_postgres
# 또는 컨테이너ID로
docker ps | grep d323f5da39a4cfb10e610d2f51187a56501fa7078a8400600b98e27cfd734cbb
```

### 2. Backend 시작
```bash
cd C:\big21\Project2
venv\Scripts\Activate.ps1
uvicorn contact_app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 브라우저 접속
```
http://localhost:8000
```

⚠️ **절대로 8001 포트 사용 금지!**

## 화면 구성

### 화면 1: 로그인/회원가입 (미로그인)
- 아이디, 비밀번호 입력
- [로그인], [가입] 버튼
- 메시지 영역

### 화면 2: 관리 (로그인됨)
**왼쪽: 연락처**
- 추가 폼: 이름, 전화, 주소, 카테고리 + [추가]
- 검색 폼: 이름 검색 + [검색], [전체]
- 목록: 이름, 전화, 주소, 종류, [수정][삭제]

**오른쪽: 카테고리**
- 입력 + [추가] 버튼
- 목록: 칩 형태 (각각 [×] 삭제)

**상단: 헤더**
- 사용자명 + [로그아웃]

**하단: 메시지**
- 성공: 초록색 1~2초
- 오류: 빨간색 유지

## 주요 함수

| 함수 | 역할 |
|------|------|
| `init()` | 로그인 상태 확인, 화면 전환 |
| `api(path, options)` | API 호출 (쿠키 자동 포함) |
| `signup()`, `login()`, `logout()` | 인증 |
| `loadContacts()`, `saveContact()`, `deleteContact()` | 연락처 CRUD |
| `loadCategories()`, `createCategory()`, `deleteCategory()` | 카테고리 CRUD |

## 코딩 규칙
- 들여쓰기: 공백 4칸
- 함수/변수: camelCase (영어)
- DOM 요소: camelCase (예: editModal)
- 이벤트 핸들러: onXxx 또는 handleXxx
- 주석: 복잡한 로직에만

## 주의사항

### API 호출
- **절대 경로**: `/auth/me`, `/contacts`, `/categories`
- **기본 포트**: 8000 (Backend)
- **에러 메시지**: 서버의 `detail` 필드만 사용

### 세션 쿠키
- HttpOnly 속성 (JS 접근 불가)
- 브라우저 자동 관리
- 모든 요청에 자동 포함

### 데이터 갱신
- 추가/수정/삭제 후 `loadContacts()` 또는 `loadCategories()` 호출
- await로 순차 처리

### 데이터 격리
- 모든 데이터 user_id로 필터링
- 다른 사용자 데이터 접근 시 404

## 개발 팁
- **F12** 개발자 도구
  - Console: 에러/로그
  - Network: API 요청/응답
  - Application: 쿠키 확인
  - Sources: 디버깅

## 테스트 계정
```
아이디: happyday
비밀번호: pass1234
```
