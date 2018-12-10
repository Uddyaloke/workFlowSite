from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import empMaster

def proceed_empMaster(request, empMaster_id, next_state_id=None):
	empmaster = get_object_or_404(empMaster, pk=empMaster_id)
	next_state = get_object_or_404(State, pk=next_state_id)

	try:
		empmaster.proceed(request.user,next_state=next_state)
		return redirect(reverse('admin:empMaster_empmaster_changelist'))

	except Exception as e:
		return HttpResponse(e.message)
