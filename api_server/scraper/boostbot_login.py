import undetected_chromedriver as uc
import pickle
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {
        "download.default_directory": "/home/eb/jupyter/pdfs",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(60)  # Set page load timeout to 60 seconds
    return driver

import time
driver = get_driver()
driver.get("https://app.boostbot.ai/login?set_lang=en")

time.sleep(1)  # Wait for a second

# Find the email input element and enter the email
email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
email_input.send_keys('yanafa9669@nasmis.com')
time.sleep(1)  # Wait for a second

# Find the password input element and enter the password
password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
password_input.send_keys('yanafa9669@nasmis.com')
time.sleep(1)  # Wait for a second

# Press Enter after entering the password
password_input.send_keys(Keys.ENTER)
time.sleep(1)  # Wait for a second

# After logging in, wait for 2 seconds before saving the cookies
time.sleep(10)
save_cookies(driver, 'cookies.pkl')
