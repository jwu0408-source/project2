import time
import os
import sys
import io

# UTF-8 인코딩 설정
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

# 스크린샷 저장 폴더
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")

# WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

screenshots = []

def take_screenshot(name, description):
    """스크린샷 캡처"""
    time.sleep(1)
    file_path = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(file_path)
    screenshots.append({
        "name": name,
        "description": description,
        "path": file_path
    })
    print(f"✅ 캡처: {name}")

try:
    print("🚀 앱 접속...")
    driver.get(base_url)
    time.sleep(2)

    # 1. 로그인 화면
    print("\n📸 1. 로그인/회원가입 화면 캡처")
    take_screenshot("01_login_screen", "초기 로그인 화면")

    # 2. 회원가입
    print("\n📸 2. 회원가입")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys("testuser")
    password_field.send_keys("pass1234")

    signup_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[0]
    signup_btn.click()
    time.sleep(2)
    take_screenshot("02_signup_message", "회원가입 완료 메시지")

    # 3. 로그인
    print("\n📸 3. 로그인")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys("testuser")
    password_field.send_keys("pass1234")

    login_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[0]
    login_btn.click()
    time.sleep(3)
    take_screenshot("03_main_screen", "로그인 후 메인 화면")

    # 4. 연락처 추가
    print("\n📸 4. 연락처 추가")
    time.sleep(2)
    try:
        wait = WebDriverWait(driver, 10)
        contact_name = wait.until(EC.presence_of_element_located((By.ID, "contact-name")))
        contact_phone = driver.find_element(By.ID, "contact-phone")
        contact_addr = driver.find_element(By.ID, "contact-addr")

        contact_name.send_keys("김철수")
        contact_phone.send_keys("01012345678")
        contact_addr.send_keys("서울시 강남구 테헤란로")

        add_contact_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[1]
        add_contact_btn.click()
        time.sleep(2)
        take_screenshot("04_add_contact", "연락처 추가 완료")
    except Exception as e:
        print(f"⚠️ 연락처 추가 건너뜀: {e}")

    # 5. 연락처 목록
    print("\n📸 5. 연락처 목록 조회")
    take_screenshot("05_contact_list", "추가된 연락처 목록")

    # 6. 연락처 검색
    print("\n📸 6. 연락처 검색")
    search_field = driver.find_element(By.ID, "search-name")
    search_field.send_keys("김")
    search_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[2]
    search_btn.click()
    time.sleep(2)
    take_screenshot("06_search_contact", "연락처 검색 결과")

    # 7. 연락처 수정
    print("\n📸 7. 연락처 수정")
    edit_btn = driver.find_element(By.CLASS_NAME, "btn-soft")
    edit_btn.click()
    time.sleep(2)
    take_screenshot("07_edit_modal", "연락처 수정 모달")

    # 수정 데이터 입력
    edit_name = driver.find_element(By.ID, "edit-modal-name")
    edit_phone = driver.find_element(By.ID, "edit-modal-phone")
    edit_addr = driver.find_element(By.ID, "edit-modal-addr")

    edit_name.clear()
    edit_phone.clear()
    edit_addr.clear()

    edit_name.send_keys("김철수")
    edit_phone.send_keys("01087654321")
    edit_addr.send_keys("서울시 강남구 삼성로")

    save_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[0]
    save_btn.click()
    time.sleep(2)
    take_screenshot("08_contact_updated", "연락처 수정 완료")

    # 8. 카테고리 추가
    print("\n📸 8. 카테고리 추가")
    category_name = driver.find_element(By.ID, "category-name")
    category_name.send_keys("직장")
    add_category_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[1]
    add_category_btn.click()
    time.sleep(2)
    take_screenshot("09_add_category", "카테고리 추가")

    # 9. 전체 목록 조회
    print("\n📸 9. 전체 목록 조회")
    all_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[1]
    all_btn.click()
    time.sleep(2)
    take_screenshot("10_full_list", "전체 연락처 목록")

    # 10. 로그아웃
    print("\n📸 10. 로그아웃")
    logout_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[0]
    logout_btn.click()
    time.sleep(2)
    take_screenshot("11_logout", "로그아웃 후 로그인 화면")

    print("\n✅ 모든 스크린샷 캡처 완료!")

except Exception as e:
    print(f"❌ 에러: {e}")

finally:
    driver.quit()

# PDF 생성
print("\n📄 PDF 파일 생성 중...")

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

doc = SimpleDocTemplate(
    "연락처_관리_웹서비스_기능설명서.pdf",
    pagesize=landscape(A4),
    rightMargin=20,
    leftMargin=20,
    topMargin=20,
    bottomMargin=20
)

styles = getSampleStyleSheet()
story = []

# 제목
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#FF6B1A'),
    spaceAfter=30,
    alignment=1
)

story.append(Paragraph("📱 연락처 관리 웹서비스", title_style))
story.append(Paragraph(f"<b>기능 설명서</b><br/>작성일: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
story.append(Spacer(1, 0.3*inch))

# 기능별 설명
features = [
    {
        "title": "1️⃣ 로그인/회원가입",
        "description": "• 신규 사용자: 아이디(영문소문자·숫자 4~20자), 비밀번호(4~20자) 입력 후 [가입]<br/>• 기존 사용자: 아이디, 비밀번호 입력 후 [로그인]<br/>• 에러/성공 메시지 표시"
    },
    {
        "title": "2️⃣ 연락처 관리",
        "description": "• <b>추가</b>: 이름, 전화번호, 주소, 카테고리 선택 후 [추가]<br/>• <b>조회</b>: 전체 연락처 목록 표시 (이름, 전화, 주소, 종류)<br/>• <b>검색</b>: 이름으로 검색 가능<br/>• <b>수정</b>: [수정] 버튼 클릭 → 모달에서 정보 수정 → [저장]<br/>• <b>삭제</b>: [삭제] 버튼 클릭 → 확인 후 삭제"
    },
    {
        "title": "3️⃣ 카테고리 관리",
        "description": "• <b>기본 카테고리</b>: 가족, 친구, 기타 (자동 생성)<br/>• <b>추가</b>: 카테고리 이름 입력 후 [추가]<br/>• <b>삭제</b>: 각 카테고리 옆 [×] 버튼으로 삭제"
    },
    {
        "title": "4️⃣ 로그아웃",
        "description": "• 우측 상단 [로그아웃] 버튼 클릭<br/>• 로그인 화면으로 복귀"
    }
]

for i, feature in enumerate(features):
    story.append(Paragraph(f"<b>{feature['title']}</b>", styles['Heading2']))
    story.append(Paragraph(feature['description'], styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

story.append(PageBreak())

# 스크린샷 추가
for screenshot in screenshots:
    try:
        # 이미지 크기 조정
        img = Image.open(screenshot['path'])
        img_width = 7.5 * inch
        img_height = img.height * (img_width / img.width)

        story.append(Paragraph(f"<b>{screenshot['description']}</b>", styles['Heading3']))
        story.append(RLImage(screenshot['path'], width=img_width, height=img_height))
        story.append(Spacer(1, 0.2*inch))
        story.append(PageBreak())
    except Exception as e:
        print(f"⚠️ 이미지 처리 실패: {screenshot['name']} - {e}")

# PDF 생성
try:
    doc.build(story)
    print("✅ PDF 파일 생성 완료: 연락처_관리_웹서비스_기능설명서.pdf")
except Exception as e:
    print(f"❌ PDF 생성 실패: {e}")
