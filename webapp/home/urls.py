"""URLS for static pages."""

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="home_index"),
    re_path(r'^[\w\d\_-]+.html$', views.page, name='home_page')
]
