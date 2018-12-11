
from django.contrib import admin
from django.urls import path, re_path

from .views import proceed_SOWRegistration

app_name = 'SOWRegistration'

urlpatterns = [
    re_path(r'^proceed_SOWRegistration/(?P<SOWRegistration_id>\d+)/(?P<next_state_id>\d+)/$', proceed_SOWRegistration, name='proceed_SOWRegistration'),
]
