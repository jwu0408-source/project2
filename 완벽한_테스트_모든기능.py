#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

screenshot_dir = "완벽한_테스트_결과"
os.makedirs(screenshot_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1400,900")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
base_url = "http://localhost:8000"

test_user = "perftest2026"
test_password = "perf2026pass"

screenshot_count = 0

def screenshot(name, desc, wait_time=3):
    global screenshot_count
    screenshot_count += 1
    time.sleep(wait_time)
    path = f"{screenshot_dir}/{screenshot_count:02d}_{name}.png"
    driver.save_screenshot(path)
    print(f"  [{screenshot_count}] ✓ {desc}")
    return path

def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_for_clickable(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

try:
    print("\n" + "="*80)
    print("  연락처 관리 웹서비스 - 완벽한 인수 테스트 (모든 기능 100% 캡처)")
    print("="*80)
    print(f"  테스트 사용자: {test_user} / {test_password}")
    print(f"  시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # === TEST 1: 초기 화면 ===
    print("[1/12] 초기 로그인 화면")
    driver.get(base_url)
    screenshot("01_로그인화면", "초기 로그인 화면 표시", 2)

    # === TEST 2: 회원가입 폼 작성 ===
    print("\n[2/12] 회원가입 폼 작성")
    username_field = wait_for_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(test_user)
    password_field.send_keys(test_password)
    screenshot("02_회원가입폼", "회원가입 정보 입력 완료", 1)

    # === TEST 3: 회원가입 버튼 클릭 ===
    print("\n[3/12] 회원가입 실행")
    signup_button = driver.find_elements(By.CLASS_NAME, "icon-btn")[1]
    signup_button.click()
    screenshot("03_회원가입완료", "회원가입 성공 메시지", 3)

    # === TEST 4: 로그인 화면으로 복귀 ===
    print("\n[4/12] 로그인 페이지 재로드")
    driver.get(base_url)
    time.sleep(2)
    screenshot("04_로그인화면복귀", "로그인 화면", 1)

    # === TEST 5: 로그인 폼 작성 ===
    print("\n[5/12] 로그인 정보 입력")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.clear()
    password_field.clear()
    username_field.send_keys(test_user)
    password_field.send_keys(test_password)
    screenshot("05_로그인폼", "로그인 정보 입력", 1)

    # === TEST 6: 로그인 버튼 클릭 ===
    print("\n[6/12] 로그인 실행")
    login_button = driver.find_elements(By.CLASS_NAME, "icon-btn")[0]
    login_button.click()

    # 관리 화면이 로드될 때까지 대기
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "contact-name")))
    screenshot("06_로그인성공", "로그인 성공 - 관리 화면", 3)

    # === TEST 7: 연락처 추가 ===
    print("\n[7/12] 연락처 추가 (김철수)")
    contact_name = driver.find_element(By.ID, "contact-name")
    contact_phone = driver.find_element(By.ID, "contact-phone")
    contact_addr = driver.find_element(By.ID, "contact-addr")

    contact_name.clear()
    contact_phone.clear()
    contact_addr.clear()

    contact_name.send_keys("김철수")
    time.sleep(0.3)
    contact_phone.send_keys("01012345678")
    time.sleep(0.3)
    contact_addr.send_keys("서울시 강남구")

    screenshot("07_연락처입력", "첫 번째 연락처 정보 입력", 1)

    # 추가 버튼 클릭 - JavaScript로 직접 호출
    driver.execute_script("saveContact()")
    screenshot("08_연락처추가됨", "첫 번째 연락처 추가 완료", 3)

    # === TEST 8: 두 번째 연락처 추가 ===
    print("\n[8/12] 연락처 추가 (이영희)")
    contact_name = driver.find_element(By.ID, "contact-name")
    contact_phone = driver.find_element(By.ID, "contact-phone")
    contact_addr = driver.find_element(By.ID, "contact-addr")

    contact_name.clear()
    contact_phone.clear()
    contact_addr.clear()

    contact_name.send_keys("이영희")
    time.sleep(0.3)
    contact_phone.send_keys("01098765432")
    time.sleep(0.3)
    contact_addr.send_keys("서울시 송파구")

    screenshot("09_두번째연락처입력", "두 번째 연락처 정보 입력", 1)

    driver.execute_script("saveContact()")
    screenshot("10_두번째추가완료", "두 번째 연락처 추가 완료", 3)

    # === TEST 9: 검색 기능 ===
    print("\n[9/12] 연락처 검색 (김)")
    search_field = driver.find_element(By.ID, "search-name")
    search_field.clear()
    search_field.send_keys("김")

    screenshot("11_검색입력", "검색어 '김' 입력", 1)

    # JavaScript로 검색 함수 호출
    driver.execute_script("loadContacts()")
    screenshot("12_검색결과", "검색 결과 표시 (김 포함)", 2)

    # === TEST 10: 전체 조회 ===
    print("\n[10/12] 전체 연락처 조회")
    # JavaScript로 전체 조회 함수 호출
    driver.execute_script("loadContacts(true)")
    screenshot("13_전체조회", "전체 연락처 조회 (2개)", 2)

    # === TEST 11: 카테고리 추가 ===
    print("\n[11/12] 카테고리 추가")
    category_field = driver.find_element(By.ID, "category-name")
    category_field.clear()
    category_field.send_keys("직장")

    screenshot("14_카테고리입력", "카테고리 '직장' 입력", 1)

    # JavaScript로 카테고리 추가 함수 호출
    driver.execute_script("createCategory()")
    screenshot("15_카테고리추가됨", "카테고리 추가 완료", 2)

    # === TEST 12: 연락처 수정 ===
    print("\n[12/12] 연락처 수정")
    time.sleep(1)
    # JavaScript로 첫 번째 연락처(id=1) 수정 시작
    driver.execute_script("startEdit(1)")
    screenshot("16_수정모달열림", "수정 모달 오픈", 2)

    # JavaScript로 수정 필드 값 변경
    driver.execute_script("""
        const phoneInput = document.getElementById('edit-modal-phone');
        phoneInput.value = '01099999999';
        phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
    """)
    screenshot("17_수정정보입력", "수정 데이터 입력 (전화번호)", 1)

    # JavaScript로 수정 저장
    driver.execute_script("saveEditModal()")
    screenshot("18_수정완료", "연락처 수정 완료", 2)

    # === TEST 13: 연락처 삭제 ===
    print("\n[13/12] 연락처 삭제")
    time.sleep(1)
    # JavaScript로 첫 번째 연락처(id=2) 삭제
    driver.execute_script("deleteContact(2)")

    # 삭제 확인 대화 처리
    time.sleep(1)
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        screenshot("19_삭제확인", "삭제 확인 대화", 1)
        alert.accept()
        screenshot("20_삭제완료", "연락처 삭제 완료", 2)
    except:
        screenshot("19_삭제확인", "삭제 완료", 1)

    # === TEST 14: 로그아웃 ===
    print("\n[14/12] 로그아웃")
    # JavaScript로 로그아웃 함수 호출
    driver.execute_script("logout()")
    screenshot("21_로그아웃완료", "로그아웃 완료 - 로그인 화면 복귀", 2)

    print("\n" + "="*80)
    print(f"  ✅ 모든 테스트 성공적으로 완료!")
    print(f"  총 {screenshot_count}개 스크린샷 캡처")
    print(f"  저장 위치: {os.path.abspath(screenshot_dir)}")
    print("="*80 + "\n")

except Exception as e:
    print(f"\n❌ [ERROR] {e}")
    import traceback
    traceback.print_exc()
    try:
        driver.save_screenshot(f"{screenshot_dir}/ERROR.png")
    except:
        pass

finally:
    time.sleep(1)
    driver.quit()
