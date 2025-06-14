import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import os

# URL of the your website 
url = 'https://XXX.com'

# Set Chrome options to enable headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set the path to chromedriver executable
chromedriver_path = '/usr/local/bin/chromedriver'

# Create a new Chrome instance
driver = webdriver.Chrome(options=chrome_options)

# Load the website
driver.get(url)

# Wait for the page to fully render
time.sleep(5)

# Extract the rendered HTML
html = driver.page_source

# Close the Chrome instance
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

data = {}

# h1〜h4のタグを取得
headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
(h1_text,h2_text,h3_text,h4_text,h5_text)=("","","","","")
for heading in headings:
    if heading.name == 'h1':
        h1_text = heading.text
        key = h1_text
    elif heading.name == 'h2':
        h2_text = heading.text
        key = f"{h1_text}-{h2_text}"
    elif heading.name == 'h3':
        h3_text = heading.text
        key = f"{h1_text}-{h2_text}-{h3_text}"
    elif heading.name == 'h4':
        h4_text = heading.text
        key = f"{h1_text}-{h2_text}-{h3_text}-{h4_text}"
    elif heading.name == 'h5':
        h5_text = heading.text
        key = f"{h1_text}-{h2_text}-{h3_text}-{h5_text}"

    # 次の要素のテキストを取得
    sibling = heading.find_next_sibling()
    value = ''
    while sibling and not sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
        value += sibling.text
        sibling = sibling.find_next_sibling()

    data[key] = value.strip()

print(len(data),(data.keys()))