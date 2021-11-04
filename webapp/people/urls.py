"""URLS for people pages."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="people_index"),
]
