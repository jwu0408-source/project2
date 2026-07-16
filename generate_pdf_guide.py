#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image as RLImage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

# 한글 폰트 등록 (Windows 기본 폰트)
try:
    # Windows 시스템 폰트 경로
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 맑은 고딕
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))
        default_font = 'MalgunGothic'
    else:
        # 대체 폰트
        pdfmetrics.registerFont(TTFont('MalgunGothic', 'C:\\Windows\\Fonts\\arial.ttf'))
        default_font = 'MalgunGothic'
except Exception as e:
    print(f"경고: 한글 폰트 등록 실패 - {e}")
    default_font = 'Helvetica'

# PDF 생성
pdf_filename = "연락처관리_웹서비스_기능설명서.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=landscape(A4),
    rightMargin=20,
    leftMargin=20,
    topMargin=20,
    bottomMargin=20
)

styles = getSampleStyleSheet()
story = []

# 커스텀 스타일
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#FF6B1A'),
    spaceAfter=10,
    alignment=1,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=14,
    textColor=colors.HexColor('#666666'),
    spaceAfter=30,
    alignment=1
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#FF6B1A'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

# 제목 페이지
story.append(Spacer(1, 1*inch))
story.append(Paragraph("📱 연락처 관리 웹서비스", title_style))
story.append(Paragraph("기능 설명서", subtitle_style))
story.append(Spacer(1, 0.5*inch))

# 기본 정보
info_data = [
    ['항목', '내용'],
    ['프로젝트명', '연락처 관리 웹서비스'],
    ['개발 언어', 'Python (FastAPI), HTML5, CSS3, JavaScript'],
    ['데이터베이스', 'PostgreSQL 16'],
    ['실행 환경', 'http://localhost:8000'],
    ['작성일', datetime.now().strftime('%Y년 %m월 %d일')]
]

info_table = Table(info_data, colWidths=[2*inch, 4*inch])
info_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B1A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 11),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
]))

story.append(info_table)
story.append(Spacer(1, 0.5*inch))

story.append(PageBreak())

# 목차
story.append(Paragraph("📋 목차", heading_style))
toc_data = [
    ['1', '로그인 / 회원가입', '3'],
    ['2', '연락처 관리', '4'],
    ['3', '카테고리 관리', '5'],
    ['4', '검색 및 필터링', '6'],
    ['5', '로그아웃', '7'],
]

toc_table = Table(toc_data, colWidths=[0.5*inch, 4.5*inch, 1*inch])
toc_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

story.append(toc_table)
story.append(Spacer(1, 0.3*inch))
story.append(PageBreak())

# 1. 로그인/회원가입
story.append(Paragraph("1️⃣ 로그인 / 회원가입", heading_style))
story.append(Paragraph(
    "<b>초기 화면</b><br/>"
    "앱 접속 시 로그인/회원가입 화면이 표시됩니다.",
    styles['Normal']
))
story.append(Spacer(1, 0.15*inch))

login_features = """
<b>기능:</b><br/>
• <b>신규 사용자</b>: 아이디(영문소문자·숫자 4~20자), 비밀번호(4~20자) 입력 → [가입] 클릭<br/>
• <b>기존 사용자</b>: 아이디, 비밀번호 입력 → [로그인] 클릭<br/>
• 입력 오류 시 빨간색 메시지 표시<br/>
• 로그인 성공 시 관리 화면으로 자동 전환
"""
story.append(Paragraph(login_features, styles['Normal']))
story.append(Spacer(1, 0.2*inch))

# 스크린샷 추가 (존재하면)
screenshot_path = "screenshots/01_login_screen.png"
if os.path.exists(screenshot_path):
    try:
        story.append(Paragraph("<b>스크린샷: 로그인 화면</b>", styles['Normal']))
        img = RLImage(screenshot_path, width=5*inch, height=3.75*inch)
        story.append(img)
    except:
        story.append(Paragraph("(스크린샷 표시 불가)", styles['Normal']))

story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 2. 연락처 관리
story.append(Paragraph("2️⃣ 연락처 관리", heading_style))

contact_features = """
<b>연락처 추가:</b><br/>
• 이름, 전화번호, 주소, 카테고리 입력 필드<br/>
• [추가] 버튼 클릭으로 새 연락처 생성<br/>
• 입력 완료 후 자동으로 목록에 추가<br/>
<br/>
<b>연락처 목록:</b><br/>
• 모든 저장된 연락처 표시<br/>
• 컬럼: 이름, 전화번호, 주소, 카테고리<br/>
• 각 행마다 [수정], [삭제] 버튼 제공<br/>
<br/>
<b>연락처 수정:</b><br/>
• [수정] 버튼 클릭 → 모달 창 열림<br/>
• 이름, 전화번호, 주소, 카테고리 수정 가능<br/>
• [저장] 또는 [취소] 선택<br/>
<br/>
<b>연락처 삭제:</b><br/>
• [삭제] 버튼 클릭<br/>
• 확인 대화 상자 표시<br/>
• 확인 시 즉시 삭제
"""
story.append(Paragraph(contact_features, styles['Normal']))
story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 3. 카테고리 관리
story.append(Paragraph("3️⃣ 카테고리 관리", heading_style))

category_features = """
<b>기본 카테고리:</b><br/>
• 회원가입 시 자동 생성: <u>가족, 친구, 기타</u><br/>
<br/>
<b>카테고리 추가:</b><br/>
• 새로운 카테고리 이름 입력<br/>
• [카테고리 추가] 버튼 클릭<br/>
• 칩(Chip) 형태로 목록에 추가<br/>
<br/>
<b>카테고리 삭제:</b><br/>
• 각 카테고리 우측의 [×] 버튼으로 삭제<br/>
• 삭제 전 확인 메시지 표시
"""
story.append(Paragraph(category_features, styles['Normal']))
story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 4. 검색 및 필터링
story.append(Paragraph("4️⃣ 검색 및 필터링", heading_style))

search_features = """
<b>이름 검색:</b><br/>
• 검색 입력 필드에 이름 또는 일부 입력<br/>
• [검색] 버튼 클릭 → 조건에 맞는 연락처만 표시<br/>
• 예: "김" 입력 → 김씨 연락처만 표시<br/>
<br/>
<b>전체 목록 보기:</b><br/>
• [전체] 버튼 클릭으로 검색 초기화<br/>
• 모든 저장된 연락처 재표시
"""
story.append(Paragraph(search_features, styles['Normal']))
story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 5. 로그아웃
story.append(Paragraph("5️⃣ 로그아웃", heading_style))

logout_features = """
<b>로그아웃:</b><br/>
• 우측 상단 [로그아웃] 버튼 클릭<br/>
• 세션 종료<br/>
• 로그인 화면으로 복귀<br/>
<br/>
<b>다시 로그인:</b><br/>
• 동일한 아이디/비밀번호로 로그인 가능<br/>
• 이전에 저장된 모든 연락처와 카테고리 복원
"""
story.append(Paragraph(logout_features, styles['Normal']))
story.append(Spacer(1, 0.5*inch))
story.append(PageBreak())

# 시스템 요구사항
story.append(Paragraph("🖥️ 시스템 요구사항", heading_style))

sys_data = [
    ['요소', '사양'],
    ['브라우저', 'Chrome, Firefox, Safari, Edge (최신 버전)'],
    ['해상도', '1920x1080 권장 (반응형 지원)'],
    ['인터넷', '로컬 네트워크 연결 필요'],
    ['데이터베이스', 'PostgreSQL 16 (Docker 컨테이너)'],
]

sys_table = Table(sys_data, colWidths=[2*inch, 4*inch])
sys_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B1A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
]))

story.append(sys_table)
story.append(Spacer(1, 0.3*inch))

# 주의사항
story.append(Paragraph("⚠️ 주의사항", heading_style))

caution = """
• <b>로그인 유지</b>: 브라우저 종료 시 로그아웃 상태가 됩니다<br/>
• <b>데이터 보안</b>: 로그인한 사용자만 자신의 데이터에 접근 가능합니다<br/>
• <b>비밀번호</b>: 분실 시 복구 불가능하므로 안전한 곳에 보관하세요<br/>
• <b>카테고리 삭제</b>: 삭제된 카테고리는 연락처에서도 제거됩니다
"""
story.append(Paragraph(caution, styles['Normal']))

# PDF 생성
try:
    doc.build(story)
    print(f"✅ PDF 생성 완료: {pdf_filename}")
    print(f"📄 파일 크기: {os.path.getsize(pdf_filename) / 1024:.1f} KB")
except Exception as e:
    print(f"❌ PDF 생성 실패: {e}")
