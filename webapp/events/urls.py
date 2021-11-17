"""URLS for event pages."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="events_index"),
    path('<int:pk>/', views.show, name='events_show'),
]
