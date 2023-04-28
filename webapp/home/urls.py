"""URLS for static pages."""

from django.urls import path, re_path

from . import api, redirects, views

urlpatterns = [
    path('', views.index, name="home_index"),
    path('about', views.about, name="home_about"),
    path('notice/dismiss', api.dismiss_notice, name="api_notice_dismiss"),
    path('notice/<notice_id>', views.notice, name="home_notice"),
    path('landing/<subdomain>', views.landing, name="home_landing"),
    path('request', views.user_request, name="user_request"),
    path('request/tool', views.user_request_tool, name="user_request_tool"),
    path('request/quota', views.user_request_quota, name="user_request_quota"),
    path('request/support',
         views.user_request_support, name="user_request_support"),
    path('request/alphafold',
         views.user_request_alphafold, name="user_request_alphafold"),
    path('aaf', views.aaf_info, name="home_aaf_info"),
    path('institutions', views.australian_institutions,
         name="home_au_institutions"),
    path('feedback/<subdomain>',
         api.subdomain_feedback,
         name="subdomain_feedback"),
    re_path(r'^[\w\d\_-]+.html$', views.page, name='home_page'),

    # Redirect
    path('galaxy', redirects.homepage, name="redirect_home"),
    path('galaxy/', redirects.homepage, name="redirect_home"),
    path('help', redirects.support, name="redirect_support"),
]
