
from django.contrib import admin
from django.urls import path, re_path

from .views import proceed_EmpRegistration

app_name = 'ManpowerManagement'

urlpatterns = [
    re_path(r'^proceed_EmpRegistration/(?P<EmpRegistration_id>\d+)/(?P<next_state_id>\d+)/$', proceed_EmpRegistration, name='proceed_EmpRegistration'),
]
