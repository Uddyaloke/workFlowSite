# # from django.core import urlresolvers
from django.http.response import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
# from django.utils.timezone import now

from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

# # Create your views here.
# from .models import workList

# def home(request):
# 	return redirect(reverse('admin:app_list', args=("workList",))+'worklist/')
# 	# return HttpResponseRedirect('/admin/workList/worklist')

@user_passes_test(lambda u: u.is_staff, login_url='/admin/workList/worklist')
def test_list(request):
    return HttpResponseRedirect('/admin/workList/worklist')
