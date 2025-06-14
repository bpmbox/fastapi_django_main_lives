# Poster
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from article_formatter import Article
from article_elements import insert_title, insert_thumbnail, insert_image_file, insert_content

class Poster:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """
        Login to Note.com
        """
        self.driver.get('https://note.com/login')
        self.driver.find_element_by_name('username').send_keys(username)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_name('login').click()

    def create_article(self, article):
        """
        Create an article
        """
        self.driver.get('https://note.com/new')
        self.driver.find_element_by_name('title').send_keys(article.title)
        self.driver.find_element_by_name('thumbnail').send_keys(article.thumbnail)
        for image_file in article.image_files:
            self.driver.find_element_by_name('image_file').send_keys(image_file)
        self.driver.find_element_by_name('content').send_keys(insert_title(article.title) + insert_thumbnail(article.thumbnail) + ''.join([insert_image_file(image_file) for image_file in article.image_files]) + insert_content(article.content))
        self.driver.find_element_by_name('hashtags').send_keys(','.join(article.hashtags))
        self.driver.find_element_by_name('price').send_keys(str(article.price))
        self.driver.find_element_by_name('scheduled_time').send_keys(article.scheduled_time)
        if article.is_paid:
            self.driver.find_element_by_name('is_paid').click()
        self.driver.find_element_by_name('post').click()

    def post_article(self, article):
        """
        Post an article
        """
        self.login(NOTE_USERNAME, NOTE_PASSWORD)
        self.create_article(article)