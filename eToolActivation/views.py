from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from river.models import State

# Create your views here.
from .models import eToolActivation

def proceed_eToolActivation(request, eToolActivation_id, next_state_id=None):
	etoolactivation = get_object_or_404(eToolActivation, pk=eToolActivation_id)
	next_state = get_object_or_404(State, pk=next_state_id)

	try:
		etoolactivation.proceed(request.user,next_state=next_state)
		return redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))
	except Exception as e:
		return HttpResponse(e.message)
