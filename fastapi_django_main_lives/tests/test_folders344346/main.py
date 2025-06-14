# Main script
from config import NOTE_USERNAME, NOTE_PASSWORD
from chrome_driver import setup_chrome_driver
from poster import Poster

def main():
    driver = setup_chrome_driver()
    poster = Poster(driver)
    article = create_article('Test Article', 'https://example.com/thumbnail.jpg', ['image1.jpg', 'image2.jpg'], 'This is a test article.', ['test', 'article'], 1000, '2023-02-20 12:00:00', True)
    poster.post_article(article)

if __name__ == '__main__':
    main()