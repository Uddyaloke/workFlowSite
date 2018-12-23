from django.contrib import admin
from django.urls import path, re_path

from .views import home

app_name = 'workList'

urlpatterns = [
    re_path(r'^/', home, name='workList'),
]