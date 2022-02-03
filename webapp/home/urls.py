"""URLS for static pages."""

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="home_index"),
    path('about', views.about, name="home_about"),
    path('support', views.support, name="home_support"),
    path('landing', views.landing, name="home_landing"),
    path('request', views.user_request, name="user_request"),
    path('request/tool', views.user_request_tool, name="user_request_tool"),
    path('request/data', views.user_request_data, name="user_request_data"),
    path('request/support',
         views.user_request_support, name="user_request_support"),
    re_path(r'^[\w\d\_-]+.html$', views.page, name='home_page'),
]
