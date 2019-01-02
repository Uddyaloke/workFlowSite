"""workFlowSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path, re_path, include, reverse_lazy,reverse
from django.views.generic.base import RedirectView

from workList.views import test_list
from .views import GeneratePdf


admin.site.site_header = 'iFlow'
admin.site.site_title = 'iFlow'
admin.site.index_title = 'Welcome to iFlow Inventory'

urlpatterns = [
    # re_path(r'^/', include('workList.urls')),
    path('admin/', admin.site.urls),
    path('admin/login', test_list),
    re_path(r'^adhocTask/', include('adhocTask.urls')),
    re_path(r'^ManpowerManagement/', include('ManpowerManagement.urls')),
    re_path(r'^eToolActivation/', include('eToolActivation.urls')),
    re_path(r'^SOWRegistration/', include('SOWRegistration.urls')),
    re_path(r'^pdf/$', GeneratePdf.as_view()),
    re_path(r'^$', RedirectView.as_view(url =reverse_lazy('admin:workList_worklist_changelist')), name="workList"),
]
