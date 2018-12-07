
from django.contrib import admin
from django.urls import path, re_path

from .views import proceed_eToolActivation

app_name = 'eToolActivation'

urlpatterns = [
    re_path(r'^proceed_eToolActivation/(?P<eToolActivation_id>\d+)/(?P<next_state_id>\d+)/$', proceed_eToolActivation, name='proceed_eToolActivation'),
]
