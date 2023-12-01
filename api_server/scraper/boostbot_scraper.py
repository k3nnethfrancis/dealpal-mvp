import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pickle
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def load_cookies(driver, path):
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

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

def parse_followers(followers_str):
    if 'M' in followers_str:
        return float(followers_str.replace('M', '').replace('+', '')) * 1e6
    elif 'K' in followers_str or 'k' in followers_str:
        return float(followers_str.replace('K', '').replace('k', '').replace('+', '')) * 1e3
    else:
        return float(followers_str.replace('+', ''))

def sort_by_followers(profiles_data):
    return sorted(profiles_data, key=lambda x: parse_followers(x['followers']), reverse=True)

def run_selenium_scraper(category):
    print("Running run_selenium_scraper function")
    # Get the driver
    driver = get_driver()
    try:
        driver.get("https://app.boostbot.ai/login?set_lang=en")
        time.sleep(1)  # Wait for a second

        # Load cookies
        load_cookies(driver, '/Users/eb/PycharmProjects/dealpal-mvp/api_server/scraper/cookies.pkl')

        # Go to the dashboard
        driver.get('https://app.boostbot.ai/dashboard')
        time.sleep(3)  # Wait for a second

        wait = WebDriverWait(driver, 10)

        # Click the button to open Instagram
        instagram_button = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'button img[alt="Instagram"]')))

        # Click on the element
        instagram_button.click()
        time.sleep(7)  # Wait for a second

        # Find the input field by its placeholder
        topic_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search for a topic"]')

        # Enter the category or topic you want to search for
        topic_input.send_keys(category)

        time.sleep(3)

        # Press Enter
        first_dropdown_item = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[id^='tag-search-result-']")))

        # Click on the first item in the dropdown list
        first_dropdown_item.click()

        # Find and click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-button"]')
        search_button.click()
        time.sleep(10)  # Wait for twenty seconds

        # Load influencers with name, handle, and statistics
        influencers = driver.find_elements(By.CSS_SELECTOR, 'table.w-full tbody tr')
        profiles_data = []
        for influencer in influencers:
            name = influencer.find_element(By.CSS_SELECTOR, 'div.font-bold').text
            handle = influencer.find_element(By.CSS_SELECTOR, 'a.line-clamp-1').text
            stats = [stat.text for stat in influencer.find_elements(By.CSS_SELECTOR, 'td.pr-4.text-right.text-sm')]
            print(f'Name: {name}, Handle: {handle}, Statistics: {stats}')

            profile_data = {
                'profile_id': handle,
                'followers': stats[0],
                'engagement': stats[2],
                'likes_per_post': stats[1],
            }
            profiles_data.append(profile_data)

        sorted_profiles_data = sort_by_followers(profiles_data)

        print(sorted_profiles_data)
        time.sleep(2)
        return sorted_profiles_data
    except Exception as e:
        print(e)
    finally:
        driver.quit()
