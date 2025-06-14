from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/<pk>/', views.scrape_website, name='scrape_website'),
]