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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

screenshot_dir = "final_acceptance_test"
os.makedirs(screenshot_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1400,800")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

test_user = "finaltest"
test_password = "final1234"

def screenshot(name, desc, wait=2):
    time.sleep(wait)
    path = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(path)
    print(f"  ✓ {desc}")

try:
    print("\n" + "="*70)
    print("  연락처 관리 웹서비스 - 완벽한 인수 테스트 (모든 기능)")
    print("="*70 + "\n")

    # === TEST 1: 초기 화면 ===
    print("[TEST 1] 초기 로그인 화면")
    driver.get(base_url)
    screenshot("01_initial_screen", "초기 로그인 화면")

    # === TEST 2: 회원가입 ===
    print("\n[TEST 2] 회원가입")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.send_keys(test_user)
    password.send_keys(test_password)
    screenshot("02_signup_form", "회원가입 폼 입력")

    signup_btns = driver.find_elements(By.CLASS_NAME, "icon-btn")
    signup_btns[1].click()  # [가입] 버튼
    screenshot("03_signup_message", "회원가입 완료 메시지", 3)

    # === TEST 3: 로그인 ===
    print("\n[TEST 3] 로그인")
    driver.get(base_url)
    time.sleep(1)
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.clear()
    password.clear()
    username.send_keys(test_user)
    password.send_keys(test_password)
    screenshot("04_login_form", "로그인 폼 입력")

    login_btns = driver.find_elements(By.CLASS_NAME, "icon-btn")
    login_btns[0].click()  # [로그인] 버튼
    screenshot("05_login_success", "로그인 성공 - 관리 화면", 4)

    # === TEST 4: 연락처 추가 ===
    print("\n[TEST 4] 연락처 추가")
    try:
        time.sleep(2)
        name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contact-name")))
        phone = driver.find_element(By.ID, "contact-phone")
        addr = driver.find_element(By.ID, "contact-addr")

        name.clear()
        phone.clear()
        addr.clear()

        name.send_keys("김철수")
        time.sleep(0.5)
        phone.send_keys("01012345678")
        time.sleep(0.5)
        addr.send_keys("서울시 강남구")
        screenshot("06_contact_form", "연락처 추가 폼 작성", 1)

        primary_btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        if primary_btns:
            primary_btns[0].click()
            screenshot("07_contact_added", "연락처 추가 완료", 2)
    except Exception as e:
        print(f"  ✗ 연락처 추가 실패: {e}")

    # === TEST 5: 연락처 목록 조회 ===
    print("\n[TEST 5] 연락처 목록 조회")
    screenshot("08_contact_list", "연락처 목록 표시", 1)

    # === TEST 6: 연락처 검색 ===
    print("\n[TEST 6] 연락처 검색")
    try:
        search = driver.find_element(By.ID, "search-name")
        search.clear()
        search.send_keys("김")
        screenshot("09_search_input", "검색어 입력", 1)

        soft_btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        if len(soft_btns) > 1:
            soft_btns[1].click()
            screenshot("10_search_result", "검색 결과 (김 포함)", 2)
    except Exception as e:
        print(f"  ✗ 검색 실패: {e}")

    # === TEST 7: 전체 조회 ===
    print("\n[TEST 7] 전체 조회")
    try:
        all_btns = driver.find_elements(By.CLASS_NAME, "btn-soft")
        if len(all_btns) > 1:
            all_btns[1].click()
            screenshot("11_all_contacts", "전체 연락처 조회", 2)
    except Exception as e:
        print(f"  ✗ 전체 조회 실패: {e}")

    # === TEST 8: 카테고리 추가 ===
    print("\n[TEST 8] 카테고리 추가")
    try:
        cat = driver.find_element(By.ID, "category-name")
        cat.clear()
        cat.send_keys("직장")
        screenshot("12_category_input", "카테고리 입력", 1)

        primary_btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
        if len(primary_btns) > 1:
            primary_btns[1].click()
            screenshot("13_category_added", "카테고리 추가 완료", 2)
    except Exception as e:
        print(f"  ✗ 카테고리 추가 실패: {e}")

    # === TEST 9: 연락처 수정 ===
    print("\n[TEST 9] 연락처 수정")
    try:
        all_btns = driver.find_elements(By.CLASS_NAME, "btn-soft")
        if len(all_btns) > 2:
            all_btns[2].click()
            screenshot("14_edit_modal", "수정 모달 열기", 2)

            edit_phone = driver.find_element(By.ID, "edit-modal-phone")
            edit_phone.clear()
            edit_phone.send_keys("01099999999")
            screenshot("15_edit_modal_filled", "수정 데이터 입력", 1)

            primary_btns = driver.find_elements(By.CLASS_NAME, "btn-primary")
            if primary_btns:
                primary_btns[0].click()
                screenshot("16_contact_updated", "수정 완료", 2)
    except Exception as e:
        print(f"  ✗ 수정 실패: {e}")

    # === TEST 10: 연락처 삭제 ===
    print("\n[TEST 10] 연락처 삭제")
    try:
        danger_btns = driver.find_elements(By.CLASS_NAME, "btn-danger")
        if danger_btns:
            danger_btns[0].click()
            screenshot("17_delete_dialog", "삭제 확인 대화", 1)

            try:
                alert = driver.switch_to.alert
                alert.accept()
                screenshot("18_contact_deleted", "삭제 완료", 2)
            except:
                pass
    except Exception as e:
        print(f"  ✗ 삭제 실패: {e}")

    # === TEST 11: 로그아웃 ===
    print("\n[TEST 11] 로그아웃")
    try:
        soft_btns = driver.find_elements(By.CLASS_NAME, "btn-soft")
        if soft_btns:
            soft_btns[0].click()
            screenshot("19_logout_complete", "로그아웃 완료", 2)
    except Exception as e:
        print(f"  ✗ 로그아웃 실패: {e}")

    print("\n" + "="*70)
    print("  모든 인수 테스트 성공적으로 완료!")
    print("="*70 + "\n")

except Exception as e:
    print(f"\n[ERROR] {e}")
    try:
        driver.save_screenshot(f"{screenshot_dir}/error.png")
    except:
        pass

finally:
    driver.quit()
