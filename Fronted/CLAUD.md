# 프론트엔드 안내

## 개요
HTML + CSS + Vanilla JavaScript로 개발된 연락처 관리 웹 앱 프론트엔드입니다.

## 프로젝트 구조
```
frontend/
├── index.html     # 로그인 페이지 (메인 화면)
├── styles.css     # 전역 스타일시트
├── app.js         # 메인 로직 및 API 연동
└── CLAUDE.md      # 이 파일
```

## 기술 스택
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)

## API 연동
- 백엔드 API: `http://localhost:8000/api`
- 로그인 엔드포인트: `POST /api/login`

## 로컬 개발 실행
1. 간단한 HTTP 서버 실행:
   ```bash
   python -m http.server 8001
   ```
2. 브라우저에서 `http://localhost:8001` 접속

## 코딩 규칙 준수
- 들여쓰기: 공백 4칸
- 함수/변수 명명: camelCase (영어)
- 주석: 필요할 때만 추가

