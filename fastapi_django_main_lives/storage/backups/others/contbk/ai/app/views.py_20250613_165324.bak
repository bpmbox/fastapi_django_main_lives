from django.shortcuts import render
from .models import WebSite
from bs4 import BeautifulSoup
import requests

def index(request):
    websites = WebSite.objects.all()
    return render(request, 'index.html', {'websites': websites})

def scrape_website(request, pk):
    website = WebSite.objects.get(pk=pk)
    url = website.url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.get_text()
    website.data = data
    website.save()
    return render(request, 'index.html', {'websites': [website]})