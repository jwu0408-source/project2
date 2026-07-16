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

# 스크린샷 저장 폴더
screenshot_dir = "final_screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1280,720")

# WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

def take_screenshot(name, description):
    """스크린샷 캡처"""
    time.sleep(1.5)
    file_path = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(file_path)
    print(f"✓ {description}")
    return file_path

try:
    print("\n=== 연락처 관리 웹서비스 완벽 테스트 시작 ===\n")

    # 1. 로그인 화면
    print("[1] 로그인 화면 캡처...")
    driver.get(base_url)
    time.sleep(3)
    take_screenshot("01_login_screen", "로그인/회원가입 화면")

    # 2. 회원가입
    print("\n[2] 회원가입 진행...")
    try:
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")

        username.clear()
        password.clear()
        username.send_keys("testuser")
        password.send_keys("test1234")

        signup_button = driver.find_elements(By.CLASS_NAME, "icon-btn")[1]
        signup_button.click()
        time.sleep(2)
        take_screenshot("02_signup_complete", "회원가입 완료 메시지")
    except Exception as e:
        print(f"회원가입 오류: {e}")

    # 3. 로그인
    print("\n[3] 로그인 진행...")
    try:
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")

        username.clear()
        password.clear()
        username.send_keys("testuser")
        password.send_keys("test1234")

        login_button = driver.find_elements(By.CLASS_NAME, "icon-btn")[0]
        login_button.click()
        time.sleep(4)
        take_screenshot("03_main_screen", "로그인 성공 - 관리 화면")
    except Exception as e:
        print(f"로그인 오류: {e}")

    # 4. 연락처 추가
    print("\n[4] 연락처 추가...")
    try:
        wait = WebDriverWait(driver, 10)
        contact_name = wait.until(EC.presence_of_element_located((By.ID, "contact-name")))
        contact_phone = driver.find_element(By.ID, "contact-phone")
        contact_addr = driver.find_element(By.ID, "contact-addr")

        contact_name.send_keys("김철수")
        contact_phone.send_keys("01012345678")
        contact_addr.send_keys("서울시 강남구")

        time.sleep(1)
        take_screenshot("04_contact_form_filled", "연락처 추가 폼 입력")

        # 추가 버튼 클릭 (연락처 추가 섹션의 버튼)
        add_buttons = driver.find_elements(By.CLASS_NAME, "btn-primary")
        add_buttons[0].click()
        time.sleep(2)
        take_screenshot("05_contact_added", "연락처 추가 완료")
    except Exception as e:
        print(f"연락처 추가 오류: {e}")

    # 5. 다른 연락처 추가
    print("\n[5] 추가 연락처 추가...")
    try:
        contact_name = driver.find_element(By.ID, "contact-name")
        contact_phone = driver.find_element(By.ID, "contact-phone")
        contact_addr = driver.find_element(By.ID, "contact-addr")

        contact_name.send_keys("이영희")
        contact_phone.send_keys("01087654321")
        contact_addr.send_keys("서울시 송파구")

        add_buttons = driver.find_elements(By.CLASS_NAME, "btn-primary")
        add_buttons[0].click()
        time.sleep(2)
    except Exception as e:
        print(f"추가 연락처 추가 오류: {e}")

    # 6. 연락처 목록
    print("\n[6] 연락처 목록 조회...")
    time.sleep(1)
    take_screenshot("06_contact_list", "연락처 목록 - 2개 추가됨")

    # 7. 검색 기능
    print("\n[7] 연락처 검색...")
    try:
        search_input = driver.find_element(By.ID, "search-name")
        search_input.send_keys("김")
        time.sleep(1)

        search_buttons = driver.find_elements(By.CLASS_NAME, "btn-primary")
        search_buttons[1].click()
        time.sleep(2)
        take_screenshot("07_search_result", "검색 결과 - '김' 검색")
    except Exception as e:
        print(f"검색 오류: {e}")

    # 8. 전체 조회
    print("\n[8] 전체 조회...")
    try:
        all_button = driver.find_elements(By.CLASS_NAME, "btn-soft")[1]
        all_button.click()
        time.sleep(2)
        take_screenshot("08_all_contacts", "전체 연락처 조회")
    except Exception as e:
        print(f"전체 조회 오류: {e}")

    # 9. 연락처 수정
    print("\n[9] 연락처 수정...")
    try:
        edit_buttons = driver.find_elements(By.CLASS_NAME, "btn-soft")
        # 첫 번째 연락처의 수정 버튼
        edit_buttons[2].click()
        time.sleep(2)
        take_screenshot("09_edit_modal_open", "수정 모달 열기")

        # 수정 진행
        edit_phone = driver.find_element(By.ID, "edit-modal-phone")
        edit_phone.clear()
        edit_phone.send_keys("01011111111")

        save_buttons = driver.find_elements(By.CLASS_NAME, "btn-primary")
        save_buttons[0].click()
        time.sleep(2)
        take_screenshot("10_contact_updated", "연락처 수정 완료")
    except Exception as e:
        print(f"수정 오류: {e}")

    # 10. 카테고리 추가
    print("\n[10] 카테고리 추가...")
    try:
        category_input = driver.find_element(By.ID, "category-name")
        category_input.send_keys("직장")
        time.sleep(1)

        add_category_buttons = driver.find_elements(By.CLASS_NAME, "btn-primary")
        add_category_buttons[1].click()
        time.sleep(2)
        take_screenshot("11_category_added", "카테고리 추가 완료")
    except Exception as e:
        print(f"카테고리 추가 오류: {e}")

    # 11. 로그아웃
    print("\n[11] 로그아웃...")
    try:
        logout_button = driver.find_elements(By.CLASS_NAME, "btn-soft")[0]
        logout_button.click()
        time.sleep(2)
        take_screenshot("12_logout_complete", "로그아웃 - 로그인 화면으로 복귀")
    except Exception as e:
        print(f"로그아웃 오류: {e}")

    print("\n=== 모든 테스트 완료 ===\n")
    print(f"스크린샷 저장 위치: {os.path.abspath(screenshot_dir)}")

except Exception as e:
    print(f"테스트 중 에러: {e}")

finally:
    driver.quit()
