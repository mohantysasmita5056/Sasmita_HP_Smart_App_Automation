# 📌 **HP Smart – Automated Account Creation (Desktop + Web Hybrid Automation)**

This project provides a complete automation workflow for creating a new **HP Smart desktop app account**, combining **Windows desktop UI automation** and **web automation** for OTP retrieval.

The automation performs:

* Opening and navigating inside the **HP Smart Windows app**
* Filling out sign-up details using **random test data**
* Opening **Mailsac** in a browser to fetch OTP using Selenium
* Extracting the 6-digit OTP from the incoming email
* Entering OTP back into HP Smart and completing account creation
* Supporting pytest execution and HTML reports


## 🚀 **What This Automation Does**

### 🔹 1. Launches HP Smart

Uses **pywinauto** to open the HP Smart desktop application and navigate to **Create Account**.

### 🔹 2. Generates Dynamic User Data

Each run creates a unique test user:

* Random first name
* Random last name
* Email pattern → `firstname.lastname.rndtest@mailsac.com`

### 🔹 3. Fills HP Smart Sign-up Form

Inputs first name, last name, email, and a predefined password.

### 🔹 4. Fetches OTP from Mailsac

Selenium WebDriver:

* Opens mailsac.com
* Enters the mailbox
* Polls for inbox messages
* Opens the latest email
* Extracts a 6-digit OTP from email body

### 🔹 5. Enters OTP Back in HP Smart

Uses clipboard paste + pywinauto to enter the OTP and submit verification.

## 🧰 **Tech Stack**

| Tool / Library         | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| **Python 3.x**         | Automation language                       |
| **pywinauto**          | Desktop UI automation for HP Smart        |
| **Selenium WebDriver** | Polling Mailsac and reading OTP emails    |
| **ChromeDriver**       | Automation engine for Chrome              |
| **pytest**             | Test runner & report support              |
| **pyperclip**          | Clipboard operations for OTP entry        |
| **Mailsac**            | Disposable mailboxes for OTP verification |


## 📁 **Project Structure**

```
hp_smart_app/
│
├── hp_smart_otp_gen.py        # Main end-to-end automation script
├── README.md               # Project documentation
├── automate_report.html    # Pytest HTML report (optional)
```

---

## ⚙️ **Environment Setup**

### 1️⃣ Install Dependencies

```bash
pip install pywinauto selenium pytest pyperclip
```

### 2️⃣ Install ChromeDriver

Ensure the ChromeDriver version matches your installed **Google Chrome**.

Place it in:

* Project folder **or**
* System PATH

### 3️⃣ Ensure HP Smart Application is Installed

Required for desktop automation.

---

## ▶️ **Running the Automation**

### Run using PyTest:

```bash
pytest test_otpfinal.py -s --html=automate_report.html
```

This will:

* Launch HP Smart
* Generate random test user
* Fill sign-up form
* Read OTP from Mailsac
* Complete verification
* Generate HTML report

---

## 🧪 **How the Tests Are Structured**

### ✔ `test_launch_hp_smart`

Launches HP Smart → Clicks **Manage HP Account** → Opens **Create Account** window.

### ✔ `test_fill_account_form`

Fills the HP account registration form inside embedded webview.

### ✔ `test_fetch_otp`

Uses Selenium to:

* Load Mailsac
* Check email inbox
* Parse and extract OTP
* Store OTP globally for next test

### ✔ `test_enter_otp`

Inputs OTP into HP Smart → Completes verification.

---

## 📝 **Configuration Constants**

You can modify these in the script:

```python
PASSWORD = "SecurePassword123"
TIMEOUT = 60
MAIL_DOMAIN = "@mailsac.com"
FIRST_NAMES = ["Santosh","Amar","Antony","Akbar","Jack"]
LAST_NAMES = ["Jens","Mohans","Pandit","kiren"]
```

## 🧩 **Key Features / Highlights**

* Works with HP Smart embedded webview (UIA Automation)
* Completely dynamic user creation each run
* OTP extraction with regex matching
* Robust waits for UI elements & inbox polling
* Modular functions + pytest fixtures
* Clipboard-based OTP entry ensures accuracy

