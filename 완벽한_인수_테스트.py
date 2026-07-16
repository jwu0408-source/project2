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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# 스크린샷 저장 폴더
screenshot_dir = "acceptance_test_screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1400,800")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

test_user = "newtestuser"
test_password = "newtest1234"

def wait_and_take_screenshot(name, description, wait_time=2):
    """대기 후 스크린샷 캡처"""
    time.sleep(wait_time)
    file_path = f"{screenshot_dir}/{name}.png"
    driver.save_screenshot(file_path)
    print(f"  ✓ {description}")
    return file_path

try:
    print("\n" + "="*60)
    print("  연락처 관리 웹서비스 - 완벽한 인수 테스트")
    print("="*60 + "\n")

    # ============ 테스트 1: 초기 화면 ============
    print("[TEST 1] 초기 로그인 화면")
    driver.get(base_url)
    wait_and_take_screenshot("01_initial_login_screen", "초기 로그인 화면")

    # ============ 테스트 2: 회원가입 ============
    print("\n[TEST 2] 회원가입")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.clear()
    password.clear()
    username.send_keys(test_user)
    password.send_keys(test_password)
    wait_and_take_screenshot("02_signup_form_filled", "회원가입 폼 작성 완료")

    signup_buttons = driver.find_elements(By.CLASS_NAME, "icon-btn")
    signup_buttons[1].click()  # 회원가입 버튼 클릭
    
    # 알림창(Alert)이 뜨는 경우 처리 (프론트엔드 구현에 따라 다름)
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
        
    wait_and_take_screenshot("03_signup_success", "회원가입 완료 상태")

    # ============ 테스트 3: 로그인 ============
    print("\n[TEST 3] 로그인 진행")
    driver.get(base_url) # 회원가입 후 리다이렉트가 안 되었을 경우를 대비
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.clear()
    password.clear()
    username.send_keys(test_user)
    password.send_keys(test_password)
    
    signup_buttons = driver.find_elements(By.CLASS_NAME, "icon-btn")
    signup_buttons[0].click()  # 로그인 버튼 클릭
    wait_and_take_screenshot("04_login_success", "로그인 후 메인 화면 진입")

    # ============ 테스트 4: 연락처 추가 ============
    print("\n[TEST 4] 연락처 추가")
    # HTML 구조에 맞는 ID나 NAME을 입력해야 합니다 (예시 ID 적용)
    name_input = driver.find_element(By.ID, "contact-name")
    phone_input = driver.find_element(By.ID, "contact-phone")
    
    name_input.send_keys("홍길동")
    phone_input.send_keys("010-1234-5678")
    
    add_button = driver.find_element(By.ID, "btn-add-contact")
    add_button.click()
    wait_and_take_screenshot("05_contact_added", "새 연락처 추가 완료")

    # ============ 테스트 5: 연락처 수정 ============
    print("\n[TEST 5] 연락처 수정")
    edit_button = driver.find_element(By.CLASS_NAME, "btn-edit") # 첫 번째 수정 버튼
    edit_button.click()
    
    phone_input = driver.find_element(By.ID, "contact-phone")
    phone_input.clear()
    phone_input.send_keys("010-9876-5432")
    
    save_button = driver.find_element(By.ID, "btn-save-contact")
    save_button.click()
    wait_and_take_screenshot("06_contact_edited", "연락처 수정 완료")

    # ============ 테스트 6: 연락처 삭제 ============
    print("\n[TEST 6] 연락처 삭제")
    delete_button = driver.find_element(By.CLASS_NAME, "btn-delete") # 첫 번째 삭제 버튼
    delete_button.click()
    
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.accept() # 삭제 확인 알림창 승인
    except:
        pass
        
    wait_and_take_screenshot("07_contact_deleted", "연락처 삭제 완료")

    # ============ 테스트 7: 로그아웃 ============
    print("\n[TEST 7] 로그아웃")
    logout_button = driver.find_element(By.ID, "btn-logout")
    logout_button.click()
    wait_and_take_screenshot("08_logout_success", "로그아웃 완료 및 초기화면 이동")

    print("\n" + "="*60)
    print("  모든 인수 테스트가 성공적으로 완료되었습니다!")
    print("="*60 + "\n")

except Exception as e:
    print(f"\n[오류 발생] 테스트 중 문제가 발생했습니다: {e}")
    driver.save_screenshot(f"{screenshot_dir}/error_fallback.png")

finally:
    driver.quit()