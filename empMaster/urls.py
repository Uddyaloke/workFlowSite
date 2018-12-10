
from django.contrib import admin
from django.urls import path, re_path

from .views import proceed_empMaster

app_name = 'empMaster'

urlpatterns = [
    re_path(r'^proceed_empMaster/(?P<empMaster_id>\d+)/(?P<next_state_id>\d+)/$', proceed_empMaster, name='proceed_empMaster'),
]
