"""URLS for news pages."""

from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.index, name="news_index"),
    path('<int:pk>/', views.show, name='news_show'),
    path('api/create', api.create_post, name='api_create_news_post'),
]
