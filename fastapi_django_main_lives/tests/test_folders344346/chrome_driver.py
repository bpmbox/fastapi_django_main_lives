# Chrome Driver setup
from selenium import webdriver

def setup_chrome_driver():
    """
    Set up Chrome Driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver