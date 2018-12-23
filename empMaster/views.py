from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import empMaster
from eToolActivation.models import eToolActivation

def proceed_empMaster(request, empMaster_id, next_state_id=None):
	empmaster = get_object_or_404(empMaster, pk=empMaster_id)
	next_state = get_object_or_404(State, pk=next_state_id)
	empmaster.updated_by = request.user
	# etoolactivation = eToolActivation.objects.filter(emp_master_id=empMaster_id)
	etoolactivation = eToolActivation.objects.filter(emp_id=empmaster.emp_id)

	try:
		empmaster.proceed(request.user,next_state=next_state)
		empmaster.save()
		if not etoolactivation and empmaster.status_id == 7:
			eToolActivation.objects.create(emp_id=empmaster.emp_id, subject='eTool Activation of ' + str(empmaster.emp_id) + ' - ' + empmaster.emp_name, created_by=empmaster.created_by, updated_by=empmaster.updated_by, account_manager=empmaster.account_manager)
		return redirect(reverse('admin:empMaster_empmaster_changelist'))

	except Exception as e:
		return HttpResponse(e.messages)
