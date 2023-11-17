import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

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
    return driver

def run_selenium(category):
    niche = category
    driver = get_driver()
    driver.get("https://ninjaoutreach.com/")
    time.sleep(1)

    search_bar = driver.find_element(By.ID, "search_input")
    search_bar.send_keys(niche)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)

    profile_ids_elements = driver.find_elements(By.CLASS_NAME, "profile-id")
    followers_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Followers')]/following-sibling::div")
    engagement_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Engagement')]/preceding-sibling::div")
    likes_per_post_elements = driver.find_elements(By.XPATH,
                                                   "//div[contains(text(), 'Likes per Post')]/preceding-sibling::div")

    profiles_data = []
    for i in range(len(profile_ids_elements)):
        profile_data = {
            'profile_id': profile_ids_elements[i].text,
            'followers': followers_elements[i].text,
            'engagement': engagement_elements[i].text,
            'likes_per_post': likes_per_post_elements[i].text,
        }
        profiles_data.append(profile_data)

    def parse_followers(followers_str):
        if 'M' in followers_str:
            return float(followers_str.replace('M', '')) * 1e6
        elif 'K' in followers_str or 'k' in followers_str:
            return float(followers_str.replace('K', '').replace('k', '')) * 1e3
        else:
            return float(followers_str)

    def sort_by_followers(profiles_data):
        return sorted(profiles_data, key=lambda x: parse_followers(x['followers']), reverse=True)

    sorted_profiles_data = sort_by_followers(profiles_data)

    return sorted_profiles_data
