# 백엔드 안내

## 개요
FastAPI 기반 REST API 서버. SQLAlchemy ORM으로 PostgreSQL과 통신하며 세션 쿠키 기반 인증을 제공합니다.
정적 파일(Frontend HTML/CSS/JS)도 함께 제공합니다.

## 기술 스택
- FastAPI (REST API)
- SQLAlchemy (ORM)
- PostgreSQL 16 (데이터베이스)
- Pydantic (검증)
- Uvicorn (ASGI 서버)

## 프로젝트 구조
```
contact_app/
├── main.py              # FastAPI 앱, 라우터 등록
├── database.py          # SQLAlchemy 설정, DB 초기화
├── models.py            # ORM 모델
├── schemas.py           # Pydantic 스키마
├── security.py          # 인증 유틸
├── crud.py              # DB 쿼리
├── routers/
│   ├── auth.py
│   ├── contacts.py
│   └── categories.py
└── static/
    └── index.html       # Frontend (HTML+CSS+JS)
```

## DB 연결

### PostgreSQL 컨테이너
- **컨테이너명**: contact_postgres
- **컨테이너ID**: `d323f5da39a4cfb10e610d2f51187a56501fa7078a8400600b98e27cfd734cbb`
- **포트**: 5559 (호스트) → 5432 (컨테이너)
- **사용자**: appuser
- **비밀번호**: 1234
- **데이터베이스**: contactdb

### 연결 URL
```
postgresql+psycopg://appuser:1234@localhost:5559/contactdb
```

### 테이블
- `users` (id, username, password_hash, created_at)
- `sessions` (id, user_id, created_at, expires_at)
- `categories` (id, user_id, name, created_at)
- `contacts` (id, user_id, category_id, name, phone, addr, created_at)

## 실행 방법

### 1. PostgreSQL 컨테이너 확인
```bash
# 컨테이너 실행 상태 확인
docker ps | grep contact_postgres

# 또는 컨테이너ID로 확인
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

## API 엔드포인트

### 인증
| 메서드 | 경로 | 설명 |
|-------|------|------|
| POST | `/auth/signup` | 회원가입 |
| POST | `/auth/login` | 로그인 |
| GET | `/auth/me` | 사용자 정보 |
| POST | `/auth/logout` | 로그아웃 |

### 연락처
| 메서드 | 경로 | 설명 |
|-------|------|------|
| GET | `/contacts` | 목록 (검색: `?name=...`) |
| POST | `/contacts` | 생성 |
| PATCH | `/contacts/{id}` | 수정 |
| DELETE | `/contacts/{id}` | 삭제 |

### 카테고리
| 메서드 | 경로 | 설명 |
|-------|------|------|
| GET | `/categories` | 목록 |
| POST | `/categories` | 생성 |
| PATCH | `/categories/{id}` | 수정 |
| DELETE | `/categories/{id}` | 삭제 |

## 보안

### 인증
- 세션 쿠키 기반 (HttpOnly, Secure)
- Argon2 비밀번호 해싱

### 인가
- 모든 쿼리에 `user_id` 필터 적용
- 다른 사용자 데이터 접근 시 404 응답

## 코딩 규칙
- 들여쓰기: 공백 4칸
- 함수/변수: camelCase (영어)
- 개발 방식: TDD/SDD

## 에러 응답

| 상태 | 설명 | 예시 |
|------|------|------|
| 401 | 미인증 | `{"detail": "not authenticated"}` |
| 404 | 없음 | `{"detail": "not found"}` |
| 409 | 중복 | `{"detail": "username already exists"}` |
| 422 | 검증 실패 | `{"detail": "validation error"}` |

## 테스트 계정

회원가입 API로 생성:
```
POST /auth/signup
{"username": "happyday", "password": "pass1234"}
```

## 주의사항
- 기본 카테고리(가족, 친구, 기타) 자동 생성 필요
- CORS: 개발 환경(모든 출처) → 프로덕션에서 변경 필요
