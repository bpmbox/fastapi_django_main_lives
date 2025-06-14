import os
import logging
from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
from app.models.product import Product
from app.services.scraping_service import ScrapingService
from app.utils.logger import logger

logger.info("Starting scraping process")

# Set up scraping service
scraping_service = ScrapingService()

# Get list of websites to scrape
websites = ["https://example.com", "https://example.net"]

# Scrape each website
for website in websites:
    logger.info(f"Scraping {website}")
    html = requests.get(website).text
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for product in soup.find_all("div", {"class": "product"}):
        product_name = product.find("h2", {"class": "product-name"}).text.strip()
        product_price = product.find("span", {"class": "product-price"}).text.strip()
        products.append(Product(product_name, product_price))
    logger.info(f"Found {len(products)} products on {website}")
    # Save products to Excel file
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"
    ws.append(["Product Name", "Product Price"])
    for product in products:
        ws.append([product.name, product.price])
    wb.save(f"{website}.xlsx")
    logger.info(f"Saved products to {website}.xlsx")