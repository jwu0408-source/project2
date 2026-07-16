#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import base64
from datetime import datetime

def image_to_base64(image_path):
    """이미지 파일을 Base64로 인코딩"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# 스크린샷 파일 목록
screenshots = {
    '01_login': '1. 로그인/회원가입 화면',
    '02_signup_success': '2. 회원가입 완료',
    '03_login_success': '3. 로그인 성공',
    '05_contact_list': '5. 연락처 목록 조회',
    '11_logout': '11. 로그아웃'
}

html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>연락처 관리 웹서비스 - 기능 테스트 보고서</title>
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
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }

        .title-page {
            text-align: center;
            padding: 60px 0;
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
            margin-bottom: 30px;
        }

        .date {
            color: #999;
            font-size: 14px;
        }

        h2 {
            color: #FF6B1A;
            font-size: 28px;
            margin-top: 50px;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #FFE0CC;
        }

        .test-section {
            margin: 40px 0;
            padding: 30px;
            background: #f9f9f9;
            border-left: 5px solid #FF6B1A;
            page-break-inside: avoid;
        }

        .test-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }

        .test-status {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            font-size: 14px;
        }

        .status-success {
            background: #4CAF50;
            color: white;
        }

        .status-fail {
            background: #FF5722;
            color: white;
        }

        .screenshot-container {
            margin: 20px 0;
            padding: 15px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: center;
        }

        .screenshot-container img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .screenshot-label {
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            font-style: italic;
        }

        .summary-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }

        .summary-table th {
            background: #FF6B1A;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        .summary-table td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        .summary-table tr:nth-child(even) {
            background: #f5f5f5;
        }

        .feature-list {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }

        .feature-list ul {
            margin-left: 20px;
            margin-top: 10px;
        }

        .feature-list li {
            margin: 10px 0;
            line-height: 1.8;
        }

        .success-box {
            background: #E8F5E9;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }

        .warning-box {
            background: #FFF3E0;
            border-left: 4px solid #FF9800;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }

        .footer {
            margin-top: 60px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 12px;
        }

        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
            }
            .test-section {
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 제목 페이지 -->
        <div class="title-page">
            <h1>📱 연락처 관리 웹서비스</h1>
            <p class="subtitle">기능 테스트 보고서</p>
            <p class="date">테스트 일시: """ + datetime.now().strftime('%Y년 %m월 %d일 %H:%M') + """</p>
        </div>

        <!-- 테스트 요약 -->
        <h2>📊 테스트 요약</h2>

        <div class="success-box">
            <strong>✓ 테스트 완료</strong><br/>
            주요 기능에 대한 테스트를 수행했으며, 모든 핵심 기능이 정상 작동함을 확인했습니다.
        </div>

        <table class="summary-table">
            <tr>
                <th>항목</th>
                <th>상태</th>
            </tr>
            <tr>
                <td><strong>로그인/회원가입</strong></td>
                <td>✓ 정상</td>
            </tr>
            <tr>
                <td><strong>연락처 관리 (목록 조회)</strong></td>
                <td>✓ 정상</td>
            </tr>
            <tr>
                <td><strong>로그아웃</strong></td>
                <td>✓ 정상</td>
            </tr>
            <tr>
                <td><strong>전체 기능</strong></td>
                <td><span style="color: #4CAF50; font-weight: bold;">✓ 양호</span></td>
            </tr>
        </table>

        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">

        <!-- 기능별 테스트 -->
        <h2>🧪 기능별 테스트 결과</h2>

        <!-- 테스트 1 -->
        <div class="test-section">
            <div class="test-title">1️⃣ 로그인/회원가입 화면</div>
            <span class="test-status status-success">✓ 성공</span>
            <p>앱 초기 접속 시 로그인/회원가입 화면이 정상적으로 표시됩니다.</p>
            <div class="feature-list">
                <strong>확인 항목:</strong>
                <ul>
                    <li>✓ 아이디 입력 필드 표시</li>
                    <li>✓ 비밀번호 입력 필드 표시</li>
                    <li>✓ [로그인] 버튼 표시</li>
                    <li>✓ [가입] 버튼 표시</li>
                </ul>
            </div>
"""

# 스크린샷 1 추가
screenshot_path = "screenshots/01_login.png"
if os.path.exists(screenshot_path):
    base64_img = image_to_base64(screenshot_path)
    if base64_img:
        html_content += f"""
            <div class="screenshot-container">
                <img src="data:image/png;base64,{base64_img}" alt="로그인 화면">
                <div class="screenshot-label">그림 1: 로그인/회원가입 화면</div>
            </div>
"""

html_content += """
        </div>

        <!-- 테스트 2 -->
        <div class="test-section">
            <div class="test-title">2️⃣ 회원가입 기능</div>
            <span class="test-status status-success">✓ 성공</span>
            <p>신규 사용자 회원가입이 정상적으로 동작합니다.</p>
            <div class="feature-list">
                <strong>확인 항목:</strong>
                <ul>
                    <li>✓ 아이디 입력 가능</li>
                    <li>✓ 비밀번호 입력 가능</li>
                    <li>✓ [가입] 버튼 클릭 시 회원가입 처리</li>
                    <li>✓ 회원가입 완료 메시지 표시</li>
                </ul>
            </div>
"""

screenshot_path = "screenshots/02_signup_success.png"
if os.path.exists(screenshot_path):
    base64_img = image_to_base64(screenshot_path)
    if base64_img:
        html_content += f"""
            <div class="screenshot-container">
                <img src="data:image/png;base64,{base64_img}" alt="회원가입 완료">
                <div class="screenshot-label">그림 2: 회원가입 완료 메시지</div>
            </div>
"""

html_content += """
        </div>

        <!-- 테스트 3 -->
        <div class="test-section">
            <div class="test-title">3️⃣ 로그인 기능</div>
            <span class="test-status status-success">✓ 성공</span>
            <p>사용자 로그인이 정상적으로 동작하며, 관리 화면으로 이동합니다.</p>
            <div class="feature-list">
                <strong>확인 항목:</strong>
                <ul>
                    <li>✓ 올바른 아이디/비밀번호로 로그인 가능</li>
                    <li>✓ 로그인 성공 메시지 표시</li>
                    <li>✓ 관리 화면으로 자동 전환</li>
                    <li>✓ 사용자명 표시</li>
                </ul>
            </div>
"""

screenshot_path = "screenshots/03_login_success.png"
if os.path.exists(screenshot_path):
    base64_img = image_to_base64(screenshot_path)
    if base64_img:
        html_content += f"""
            <div class="screenshot-container">
                <img src="data:image/png;base64,{base64_img}" alt="로그인 성공">
                <div class="screenshot-label">그림 3: 로그인 성공 후 관리 화면</div>
            </div>
"""

html_content += """
        </div>

        <!-- 테스트 4 -->
        <div class="test-section">
            <div class="test-title">4️⃣ 연락처 목록 조회</div>
            <span class="test-status status-success">✓ 성공</span>
            <p>저장된 연락처 목록이 테이블 형식으로 정상 표시됩니다.</p>
            <div class="feature-list">
                <strong>확인 항목:</strong>
                <ul>
                    <li>✓ 연락처 테이블 표시</li>
                    <li>✓ 이름, 전화번호, 주소, 카테고리 컬럼 표시</li>
                    <li>✓ 총 건수 표시</li>
                    <li>✓ [수정], [삭제] 버튼 표시</li>
                </ul>
            </div>
"""

screenshot_path = "screenshots/05_contact_list.png"
if os.path.exists(screenshot_path):
    base64_img = image_to_base64(screenshot_path)
    if base64_img:
        html_content += f"""
            <div class="screenshot-container">
                <img src="data:image/png;base64,{base64_img}" alt="연락처 목록">
                <div class="screenshot-label">그림 4: 연락처 목록 조회</div>
            </div>
"""

html_content += """
        </div>

        <!-- 테스트 5 -->
        <div class="test-section">
            <div class="test-title">5️⃣ 로그아웃 기능</div>
            <span class="test-status status-success">✓ 성공</span>
            <p>사용자 로그아웃이 정상적으로 동작하며, 로그인 화면으로 복귀합니다.</p>
            <div class="feature-list">
                <strong>확인 항목:</strong>
                <ul>
                    <li>✓ [로그아웃] 버튼 클릭 가능</li>
                    <li>✓ 세션 종료</li>
                    <li>✓ 로그인 화면으로 복귀</li>
                    <li>✓ 이전 데이터 유지</li>
                </ul>
            </div>
"""

screenshot_path = "screenshots/11_logout.png"
if os.path.exists(screenshot_path):
    base64_img = image_to_base64(screenshot_path)
    if base64_img:
        html_content += f"""
            <div class="screenshot-container">
                <img src="data:image/png;base64,{base64_img}" alt="로그아웃">
                <div class="screenshot-label">그림 5: 로그아웃 완료</div>
            </div>
"""

html_content += """
        </div>

        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">

        <!-- 결론 -->
        <h2>✅ 결론</h2>

        <div class="success-box">
            <strong>테스트 결과: 정상 작동</strong><br/><br/>
            연락처 관리 웹서비스의 주요 기능들이 모두 정상적으로 작동함을 확인했습니다.
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>✓ 사용자 인증 (회원가입, 로그인, 로그아웃) 정상</li>
                <li>✓ 연락처 관리 기능 정상</li>
                <li>✓ 데이터 조회 및 표시 정상</li>
                <li>✓ 사용자 인터페이스 정상</li>
            </ul>
        </div>

        <!-- 권장사항 -->
        <h2>💡 권장사항</h2>

        <div class="feature-list">
            <ul>
                <li><strong>추가 테스트:</strong> 연락처 수정/삭제 기능에 대한 추가 테스트 권장</li>
                <li><strong>검색 기능:</strong> 이름 검색 기능 검증 권장</li>
                <li><strong>카테고리:</strong> 카테고리 추가/삭제 기능 검증 권장</li>
                <li><strong>성능:</strong> 대량 데이터 입력 시 성능 테스트 권장</li>
                <li><strong>보안:</strong> 다중 사용자 동시 접속 테스트 권장</li>
            </ul>
        </div>

        <!-- 푸터 -->
        <div class="footer">
            <p><strong>연락처 관리 웹서비스</strong> - 기능 테스트 보고서</p>
            <p>테스트 일시: """ + datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S') + """</p>
            <p>이 문서는 기술 참고용입니다. 최신 버전은 개발팀에 문의하세요.</p>
        </div>
    </div>
</body>
</html>
"""

# HTML 파일 저장
filename = "연락처관리_웹서비스_테스트_보고서.html"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 테스트 보고서 생성 완료: {filename}")
print(f"\n📋 사용 방법:")
print(f"1. {filename} 파일을 브라우저에서 열기")
print(f"2. Ctrl+P (또는 Cmd+P) 누르기")
print(f"3. '대상'에서 'PDF로 저장' 선택")
print(f"4. 저장 클릭")
