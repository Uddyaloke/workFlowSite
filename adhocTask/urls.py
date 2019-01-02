
from django.contrib import admin
from django.urls import path, re_path

from .views import proceed_adhocTask

app_name = 'adhocTask'

urlpatterns = [
    re_path(r'^proceedhocTask/(?P<adhocTask_id>\d+)/(?P<next_state_id>\d+)/$', proceed_adhocTask, name='proceed_adhocTask'),
]