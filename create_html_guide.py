#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>연락처 관리 웹서비스 기능설명서</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }

        .title-page {
            text-align: center;
            padding: 100px 0;
            border-bottom: 3px solid #FF6B1A;
            margin-bottom: 50px;
        }

        h1 {
            color: #FF6B1A;
            font-size: 48px;
            margin-bottom: 20px;
        }

        .subtitle {
            color: #666;
            font-size: 24px;
            margin-bottom: 50px;
        }

        .date {
            color: #999;
            font-size: 14px;
        }

        h2 {
            color: #FF6B1A;
            font-size: 24px;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #FFE0CC;
        }

        h3 {
            color: #333;
            font-size: 18px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0 30px 0;
        }

        .info-table th {
            background: #FF6B1A;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        .info-table td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        .info-table tr:nth-child(even) {
            background: #f9f9f9;
        }

        .feature-box {
            background: #f9f9f9;
            border-left: 4px solid #FF6B1A;
            padding: 15px;
            margin: 20px 0;
        }

        .feature-box ul {
            margin-left: 20px;
            margin-top: 10px;
        }

        .feature-box li {
            margin: 8px 0;
            line-height: 1.8;
        }

        .section {
            page-break-after: always;
            padding-bottom: 40px;
            min-height: 500px;
        }

        .caution {
            background: #FFF3E0;
            border: 2px solid #FF9800;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }

        .caution h3 {
            color: #FF6B1A;
            margin-top: 0;
        }

        .toc {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }

        .toc ol {
            margin-left: 20px;
        }

        .toc li {
            margin: 10px 0;
        }

        p {
            margin: 15px 0;
            line-height: 1.8;
        }

        strong {
            color: #333;
        }

        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
                max-width: 100%;
            }
            .section {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 제목 페이지 -->
        <div class="title-page">
            <h1>📱 연락처 관리 웹서비스</h1>
            <p class="subtitle">기능 설명서</p>
            <p class="date">작성일: """ + datetime.now().strftime('%Y년 %m월 %d일') + """</p>
        </div>

        <!-- 기본 정보 -->
        <h2>📋 프로젝트 정보</h2>
        <table class="info-table">
            <tr>
                <th>항목</th>
                <th>내용</th>
            </tr>
            <tr>
                <td><strong>프로젝트명</strong></td>
                <td>연락처 관리 웹서비스</td>
            </tr>
            <tr>
                <td><strong>개발 언어</strong></td>
                <td>Python (FastAPI), HTML5, CSS3, JavaScript</td>
            </tr>
            <tr>
                <td><strong>데이터베이스</strong></td>
                <td>PostgreSQL 16</td>
            </tr>
            <tr>
                <td><strong>실행 환경</strong></td>
                <td>http://localhost:8000</td>
            </tr>
            <tr>
                <td><strong>Docker 컨테이너</strong></td>
                <td>contact_postgres (포트 5559)</td>
            </tr>
        </table>

        <!-- 목차 -->
        <h2>📑 목차</h2>
        <div class="toc">
            <ol>
                <li>로그인 / 회원가입</li>
                <li>연락처 관리</li>
                <li>카테고리 관리</li>
                <li>검색 및 필터링</li>
                <li>로그아웃</li>
                <li>시스템 요구사항</li>
                <li>주의사항</li>
            </ol>
        </div>

        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">

        <!-- 섹션 1: 로그인/회원가입 -->
        <div class="section">
            <h2>1️⃣ 로그인 / 회원가입</h2>

            <h3>초기 화면</h3>
            <p>앱 접속 시 로그인/회원가입 화면이 표시됩니다.</p>

            <div class="feature-box">
                <h3 style="margin-top: 0;">기능</h3>
                <ul>
                    <li><strong>신규 사용자:</strong> 아이디(영문소문자·숫자 4~20자), 비밀번호(4~20자) 입력 → [가입] 클릭</li>
                    <li><strong>기존 사용자:</strong> 아이디, 비밀번호 입력 → [로그인] 클릭</li>
                    <li>입력 오류 시 빨간색 메시지 표시</li>
                    <li>로그인 성공 시 관리 화면으로 자동 전환</li>
                    <li>로그인 성공 시 초록색 "로그인 성공" 메시지 2초 표시</li>
                </ul>
            </div>
        </div>

        <!-- 섹션 2: 연락처 관리 -->
        <div class="section">
            <h2>2️⃣ 연락처 관리</h2>

            <h3>연락처 추가</h3>
            <div class="feature-box">
                <ul>
                    <li>이름, 전화번호, 주소, 카테고리 입력 필드</li>
                    <li>[추가] 버튼 클릭으로 새 연락처 생성</li>
                    <li>입력 완료 후 자동으로 목록에 추가</li>
                    <li>필드 자동 초기화</li>
                </ul>
            </div>

            <h3>연락처 목록</h3>
            <div class="feature-box">
                <ul>
                    <li>모든 저장된 연락처 표시</li>
                    <li>컬럼: 이름, 전화번호, 주소, 카테고리</li>
                    <li>각 행마다 [수정], [삭제] 버튼 제공</li>
                    <li>총 건수 표시 (예: "총 5건")</li>
                </ul>
            </div>

            <h3>연락처 수정</h3>
            <div class="feature-box">
                <ul>
                    <li>[수정] 버튼 클릭 → 모달 창 열림</li>
                    <li>이름, 전화번호, 주소, 카테고리 수정 가능</li>
                    <li>[저장] 또는 [취소] 선택</li>
                    <li>저장 시 목록 자동 갱신</li>
                </ul>
            </div>

            <h3>연락처 삭제</h3>
            <div class="feature-box">
                <ul>
                    <li>[삭제] 버튼 클릭</li>
                    <li>확인 대화 상자 표시 ("삭제하시겠습니까?")</li>
                    <li>확인 시 즉시 삭제</li>
                </ul>
            </div>
        </div>

        <!-- 섹션 3: 카테고리 관리 -->
        <div class="section">
            <h2>3️⃣ 카테고리 관리</h2>

            <h3>기본 카테고리</h3>
            <div class="feature-box">
                <ul>
                    <li>회원가입 시 자동 생성: <strong>가족, 친구, 기타</strong></li>
                    <li>칩(Chip) 형태로 표시</li>
                </ul>
            </div>

            <h3>카테고리 추가</h3>
            <div class="feature-box">
                <ul>
                    <li>새로운 카테고리 이름 입력</li>
                    <li>[카테고리 추가] 버튼 클릭</li>
                    <li>칩(Chip) 형태로 목록에 추가</li>
                    <li>입력 필드 자동 초기화</li>
                </ul>
            </div>

            <h3>카테고리 삭제</h3>
            <div class="feature-box">
                <ul>
                    <li>각 카테고리 우측의 [×] 버튼으로 삭제</li>
                    <li>삭제 전 확인 메시지 표시</li>
                    <li>삭제 시 해당 카테고리가 지정된 연락처도 함께 갱신</li>
                </ul>
            </div>
        </div>

        <!-- 섹션 4: 검색 및 필터링 -->
        <div class="section">
            <h2>4️⃣ 검색 및 필터링</h2>

            <h3>이름 검색</h3>
            <div class="feature-box">
                <ul>
                    <li>검색 입력 필드에 이름 또는 일부 입력</li>
                    <li>[검색] 버튼 클릭 → 조건에 맞는 연락처만 표시</li>
                    <li>예: "김" 입력 → 이름에 "김"이 포함된 연락처만 표시</li>
                    <li>실시간 검색 지원</li>
                </ul>
            </div>

            <h3>전체 목록 보기</h3>
            <div class="feature-box">
                <ul>
                    <li>[전체] 버튼 클릭으로 검색 초기화</li>
                    <li>모든 저장된 연락처 재표시</li>
                    <li>검색 입력 필드 자동 비움</li>
                </ul>
            </div>
        </div>

        <!-- 섹션 5: 로그아웃 -->
        <div class="section">
            <h2>5️⃣ 로그아웃</h2>

            <h3>로그아웃 절차</h3>
            <div class="feature-box">
                <ul>
                    <li>우측 상단 [로그아웃] 버튼 클릭</li>
                    <li>세션 종료</li>
                    <li>로그인 화면으로 복귀</li>
                </ul>
            </div>

            <h3>다시 로그인</h3>
            <div class="feature-box">
                <ul>
                    <li>동일한 아이디/비밀번호로 로그인 가능</li>
                    <li>이전에 저장된 모든 연락처와 카테고리 복원</li>
                    <li>사용자별 데이터 완전 격리</li>
                </ul>
            </div>
        </div>

        <!-- 섹션 6: 시스템 요구사항 -->
        <div class="section">
            <h2>🖥️ 시스템 요구사항</h2>

            <table class="info-table">
                <tr>
                    <th>요소</th>
                    <th>사양</th>
                </tr>
                <tr>
                    <td><strong>브라우저</strong></td>
                    <td>Chrome, Firefox, Safari, Edge (최신 버전)</td>
                </tr>
                <tr>
                    <td><strong>해상도</strong></td>
                    <td>1920x1080 권장 (반응형 지원)</td>
                </tr>
                <tr>
                    <td><strong>인터넷</strong></td>
                    <td>로컬 네트워크 연결 필요</td>
                </tr>
                <tr>
                    <td><strong>데이터베이스</strong></td>
                    <td>PostgreSQL 16 (Docker 컨테이너)</td>
                </tr>
                <tr>
                    <td><strong>운영체제</strong></td>
                    <td>Windows, macOS, Linux</td>
                </tr>
            </table>
        </div>

        <!-- 섹션 7: 주의사항 -->
        <div class="section">
            <h2>⚠️ 주의사항</h2>

            <div class="caution">
                <h3>데이터 보안</h3>
                <ul>
                    <li>로그인한 사용자만 자신의 데이터에 접근 가능합니다</li>
                    <li>각 사용자의 데이터는 완전히 격리됩니다</li>
                    <li>다른 사용자의 연락처 조회는 불가능합니다</li>
                </ul>
            </div>

            <div class="caution">
                <h3>비밀번호 관리</h3>
                <ul>
                    <li>분실 시 복구 불가능하므로 안전한 곳에 보관하세요</li>
                    <li>비밀번호는 암호화되어 저장됩니다</li>
                    <li>강력한 비밀번호 사용을 권장합니다</li>
                </ul>
            </div>

            <div class="caution">
                <h3>세션 관리</h3>
                <ul>
                    <li>브라우저 종료 시 로그아웃 상태가 될 수 있습니다</li>
                    <li>장시간 사용하지 않을 경우 자동 로그아웃될 수 있습니다</li>
                </ul>
            </div>

            <div class="caution">
                <h3>카테고리 관리</h3>
                <ul>
                    <li>삭제된 카테고리는 연락처에서도 제거됩니다</li>
                    <li>기본 카테고리(가족, 친구, 기타) 삭제 후 재생성 시 초기 설정으로 복구됩니다</li>
                </ul>
            </div>
        </div>

        <!-- 푸터 -->
        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">
        <div style="text-align: center; color: #999; font-size: 12px; padding: 20px 0;">
            <p>연락처 관리 웹서비스 - 기능설명서</p>
            <p>작성일: """ + datetime.now().strftime('%Y년 %m월 %d일') + """</p>
            <p>이 문서는 기술 참고용입니다. 최신 버전은 개발팀에 문의하세요.</p>
        </div>
    </div>

    <script>
        // 인쇄 시 자동으로 PDF로 저장 옵션 제공
        window.addEventListener('load', function() {
            console.log('PDF로 저장하려면: Ctrl+P (또는 Cmd+P) → PDF로 저장 선택');
        });
    </script>
</body>
</html>
"""

# HTML 파일 저장
filename = "연락처관리_웹서비스_기능설명서.html"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML 파일 생성 완료: {filename}")
print(f"\n📋 사용 방법:")
print(f"1. {filename} 파일을 브라우저에서 열기")
print(f"2. Ctrl+P (또는 Cmd+P) 누르기")
print(f"3. '대상'에서 'PDF로 저장' 선택")
print(f"4. 저장 클릭")
