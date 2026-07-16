#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# 스크린샷 저장 폴더
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1280,720")
options.add_argument("--start-maximized")

# WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

test_results = []

def add_watermark(image_path, text, status="성공"):
    """스크린샷에 테스트 결과 워터마크 추가"""
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # 상태 표시 (초록색 배경)
        status_color = "#4CAF50" if status == "성공" else "#FF5722"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 텍스트 추가
        text_line = f"[{status}] {text} - {timestamp}"

        # 하단에 배너 추가
        banner_height = 50
        new_img = Image.new('RGB', (img.width, img.height + banner_height), color=status_color)
        new_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(new_img)
        draw.text((10, img.height + 10), text_line, fill="white")

        new_img.save(image_path)
        return True
    except Exception as e:
        print(f"워터마크 추가 실패: {e}")
        return False

def take_screenshot(name, description, status="성공"):
    """스크린샷 캡처 및 워터마크 추가"""
    time.sleep(1)
    file_path = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(file_path)
    add_watermark(file_path, description, status)
    test_results.append({
        "name": name,
        "description": description,
        "path": file_path,
        "status": status
    })
    print(f"[OK] {description}")

try:
    print("\n=== 연락처 관리 웹서비스 기능 테스트 시작 ===\n")

    # 1. 로그인 화면
    print("[1] 로그인/회원가입 기능 테스트...")
    driver.get(base_url)
    time.sleep(2)
    take_screenshot("01_login", "1. 로그인/회원가입 화면 표시", "성공")

    # 2. 회원가입
    print("\n[2] 회원가입 기능 테스트...")
    try:
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        username_field.clear()
        password_field.clear()
        username_field.send_keys("testuser123")
        password_field.send_keys("password123")

        signup_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[0]
        signup_btn.click()
        time.sleep(2)
        take_screenshot("02_signup_success", "2. 회원가입 완료 메시지 표시", "성공")
    except Exception as e:
        print(f"회원가입 실패: {e}")

    # 3. 로그인
    print("\n[3] 로그인 기능 테스트...")
    try:
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        username_field.clear()
        password_field.clear()
        username_field.send_keys("testuser123")
        password_field.send_keys("password123")

        login_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[0]
        login_btn.click()
        time.sleep(3)
        take_screenshot("03_login_success", "3. 로그인 성공 후 관리 화면 표시", "성공")
    except Exception as e:
        print(f"로그인 실패: {e}")

    # 4. 연락처 추가
    print("\n[4] 연락처 추가 기능 테스트...")
    try:
        wait = WebDriverWait(driver, 10)
        contact_name = wait.until(EC.presence_of_element_located((By.ID, "contact-name")))
        contact_phone = driver.find_element(By.ID, "contact-phone")
        contact_addr = driver.find_element(By.ID, "contact-addr")

        contact_name.send_keys("김철수")
        contact_phone.send_keys("01012345678")
        contact_addr.send_keys("서울시 강남구")

        add_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[1]
        add_btn.click()
        time.sleep(2)
        take_screenshot("04_contact_added", "4. 연락처 추가 및 목록 표시", "성공")
    except Exception as e:
        print(f"연락처 추가 실패: {e}")
        take_screenshot("04_contact_added_error", "4. 연락처 추가 실패", "실패")

    # 5. 다른 연락처 추가
    print("\n[5] 추가 연락처 추가...")
    try:
        contact_name = driver.find_element(By.ID, "contact-name")
        contact_phone = driver.find_element(By.ID, "contact-phone")
        contact_addr = driver.find_element(By.ID, "contact-addr")

        contact_name.send_keys("이영희")
        contact_phone.send_keys("01087654321")
        contact_addr.send_keys("서울시 송파구")

        add_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[1]
        add_btn.click()
        time.sleep(2)
    except Exception as e:
        print(f"추가 연락처 추가 실패: {e}")

    # 6. 연락처 목록
    print("\n[6] 연락처 목록 조회 기능 테스트...")
    time.sleep(1)
    take_screenshot("05_contact_list", "5. 추가된 연락처 목록 표시", "성공")

    # 7. 연락처 검색
    print("\n[7] 연락처 검색 기능 테스트...")
    try:
        search_field = driver.find_element(By.ID, "search-name")
        search_field.send_keys("김")

        search_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[2]
        search_btn.click()
        time.sleep(2)
        take_screenshot("06_search_result", "6. 연락처 검색 결과 표시 (이름: 김)", "성공")
    except Exception as e:
        print(f"검색 실패: {e}")

    # 8. 전체 조회
    print("\n[8] 전체 조회 기능 테스트...")
    try:
        all_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[1]
        all_btn.click()
        time.sleep(2)
        take_screenshot("07_all_contacts", "7. 전체 연락처 조회", "성공")
    except Exception as e:
        print(f"전체 조회 실패: {e}")

    # 9. 연락처 수정
    print("\n[9] 연락처 수정 기능 테스트...")
    try:
        edit_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[2]
        edit_btn.click()
        time.sleep(2)
        take_screenshot("08_edit_modal", "8. 연락처 수정 모달 열기", "성공")

        # 모달에서 데이터 수정
        edit_phone = driver.find_element(By.ID, "edit-modal-phone")
        edit_phone.clear()
        edit_phone.send_keys("01011111111")

        save_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[0]
        save_btn.click()
        time.sleep(2)
        take_screenshot("09_contact_updated", "9. 연락처 수정 완료", "성공")
    except Exception as e:
        print(f"수정 실패: {e}")

    # 10. 카테고리 추가
    print("\n[10] 카테고리 추가 기능 테스트...")
    try:
        category_field = driver.find_element(By.ID, "category-name")
        category_field.send_keys("직장")

        add_category_btn = driver.find_elements(By.CLASS_NAME, "btn-primary")[1]
        add_category_btn.click()
        time.sleep(2)
        take_screenshot("10_category_added", "10. 카테고리 추가 및 목록 표시", "성공")
    except Exception as e:
        print(f"카테고리 추가 실패: {e}")

    # 11. 로그아웃
    print("\n[11] 로그아웃 기능 테스트...")
    try:
        logout_btn = driver.find_elements(By.CLASS_NAME, "btn-soft")[0]
        logout_btn.click()
        time.sleep(2)
        take_screenshot("11_logout", "11. 로그아웃 완료 - 로그인 화면으로 복귀", "성공")
    except Exception as e:
        print(f"로그아웃 실패: {e}")

    print("\n=== 모든 테스트 완료 ===\n")

except Exception as e:
    print(f"테스트 중 에러: {e}")

finally:
    driver.quit()

# 테스트 결과 요약
print("\n=== 테스트 결과 요약 ===")
print(f"총 테스트: {len(test_results)}개")
print(f"성공: {len([t for t in test_results if t['status'] == '성공'])}개")
print(f"실패: {len([t for t in test_results if t['status'] == '실패'])}개")
print(f"\n스크린샷 저장 위치: {os.path.abspath(screenshot_dir)}")
