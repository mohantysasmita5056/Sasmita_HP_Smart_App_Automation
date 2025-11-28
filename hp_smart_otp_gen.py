import pytest
import time
import random
import string
import re
import pyperclip
from pywinauto import Desktop, keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- CONFIG ----------------
PASSWORD = "SecurePassword123"
TIMEOUT = 60
MAIL_DOMAIN = "@mailsac.com"
FIRST_NAMES = ["Santosh","Amar","Antony","Akbar","Jack"]
LAST_NAMES = ["Jens","Mohans","Pandit","kiren"]

# ---------------- HELPERS ----------------
def get_random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def generate_random_mailbox():
    return ''.join(random.choices(string.ascii_lowercase, k=4)) + "test"

def build_email(first, last):
    suffix = generate_random_mailbox()
    mailbox = f"{first.lower()}.{last.lower()}.{suffix}"
    return f"{mailbox}@mailsac.com", mailbox

# ---------------- FIXTURES ----------------
@pytest.fixture(scope="session")
def desktop():
    return Desktop(backend="uia")

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.fixture(scope="session")
def user_data():
    first, last = get_random_name()
    email, mailbox = build_email(first, last)
    return {"first": first, "last": last, "email": email, "mailbox": mailbox}

# ---------------- TESTS ----------------
def test_launch_hp_smart(desktop):
    keyboard.send_keys("{VK_LWIN}HP Smart{ENTER}")
    main_win = desktop.window(title="HP Smart")
    main_win.wait('exists visible enabled ready', timeout=TIMEOUT)
    assert main_win.exists(), "HP Smart main window not found"

    manage_btn = main_win.child_window(title="Manage HP Account", auto_id="HpcSignedOutIcon", control_type="Button")
    manage_btn.wait('visible enabled ready', timeout=TIMEOUT)
    manage_btn.click_input()

    create_btn = main_win.child_window(auto_id="HpcSignOutFlyout_CreateBtn", control_type="Button")
    create_btn.wait('visible enabled ready', timeout=TIMEOUT)
    create_btn.click_input()
    assert create_btn.exists(), "Create Account button not clicked"

def test_fill_account_form(desktop, user_data):
    browser_win = desktop.window(title_re=".*HP account.*")
    browser_win.wait('exists visible enabled ready', timeout=TIMEOUT)
    assert browser_win.exists(), "HP Account browser window not found"

    browser_win.child_window(auto_id="firstName", control_type="Edit").type_keys(user_data["first"])
    browser_win.child_window(auto_id="lastName", control_type="Edit").type_keys(user_data["last"])
    browser_win.child_window(auto_id="email", control_type="Edit").type_keys(user_data["email"])
    browser_win.child_window(auto_id="password", control_type="Edit").type_keys(PASSWORD)

    create_btn = browser_win.child_window(auto_id="sign-up-submit", control_type="Button")
    create_btn.wait('visible enabled ready', timeout=TIMEOUT)
    create_btn.click_input()
    time.sleep(6)

def test_fetch_otp(driver, user_data):
    driver.get("https://mailsac.com")
    wait = WebDriverWait(driver, 20)

    mailbox_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='mailbox']")))
    mailbox_field.send_keys(user_data["mailbox"])

    check_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Check the mail!']")))
    check_btn.click()

    start_time = time.time()
    otp = None
    while time.time() - start_time < 60:
        try:
            email_row = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'inbox-table')]/tbody/tr[contains(@class,'clickable')][1]"))
            )
            email_row.click()
            break
        except:
            driver.find_element(By.XPATH, "//button[normalize-space()='Check the mail!']").click()

    body_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#emailBody")))
    email_body = body_elem.text
    otp_match = re.search(r"\b(\d{6})\b", email_body)
    assert otp_match, "Failed to fetch OTP from email"
    pytest.otp = otp_match.group(1)

def test_enter_otp(desktop):
    otp = getattr(pytest, 'otp', None)
    assert otp is not None, "OTP not available for verification"

    otp_win = desktop.window(title_re=".*HP account.*")
    otp_win.wait('exists visible enabled ready', timeout=TIMEOUT)
    assert otp_win.exists(), "OTP window not found"

    otp_box = otp_win.child_window(auto_id="code", control_type="Edit")
    otp_box.wait('visible enabled ready', timeout=10)

    pyperclip.copy(otp)
    time.sleep(1)
    otp_box.click_input()
    otp_box.type_keys("^v")

    verify_btn = otp_win.child_window(auto_id="submit-code", control_type="Button")
    verify_btn.wait('visible enabled ready', timeout=TIMEOUT)
    verify_btn.click_input()
    time.sleep(4)
