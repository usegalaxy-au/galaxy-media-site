"""URLS for news pages."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="news_index"),
    path('<int:pk>/', views.show, name='news_show'),
]
