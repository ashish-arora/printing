__author__ = 'ashish'

from django.conf.urls import patterns, include, url

from django.contrib import admin
#admin.autodiscover()
from printapp import web_views

from django.conf.urls import url, include
from printapp.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^index', login_required(web_views.IndexView.as_view(), login_url='/login')),
    url(r'^dashboard', login_required(web_views.DashboardView.as_view(), login_url='/login')),
    url(r'^login', web_views.LoginView.as_view()),
    url(r'^logout', web_views.LogoutView.as_view()),
    url(r'^signup', web_views.SignUpView.as_view()),
    url(r'^request/$', web_views.RequestView.as_view()),
    url(r'^request/(?P<request_id>.*)/$', web_views.SingleRequestView.as_view()),
    url(r'^request/(?P<request_id>.*)/response', web_views.ResponseView.as_view()),

)

