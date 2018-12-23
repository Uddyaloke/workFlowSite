from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import eToolActivation

def proceed_eToolActivation(request, eToolActivation_id, next_state_id=None):
	etoolactivation = get_object_or_404(eToolActivation, pk=eToolActivation_id)
	next_state = get_object_or_404(State, pk=next_state_id)
	etoolactivation.updated_by = request.user

	try:
		if etoolactivation.status_id == 1:
			if etoolactivation.team_lead_check_list_1 == True and  etoolactivation.team_lead_check_list_2 == True and etoolactivation.team_lead_check_list_3 == True and etoolactivation.team_lead_check_list_4 == True and etoolactivation.team_lead_check_list_5 == True:
				# etoolactivation.motion_date = timezone.now()
				# etoolactivation.save()
				etoolactivation.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))
			else:
					return 	redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))

		elif etoolactivation.status_id == 2:
			if etoolactivation.spoc_check_list_1 == True and  etoolactivation.spoc_check_list_2 == True and etoolactivation.spoc_check_list_3 == True and etoolactivation.spoc_check_list_4 == True and etoolactivation.spoc_check_list_5 == True:
				etoolactivation.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))
			else:
				return 	redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))

		elif etoolactivation.team_lead_check_list_1 == True and  etoolactivation.team_lead_check_list_2 == True and etoolactivation.team_lead_check_list_3 == True and etoolactivation.team_lead_check_list_4 == True and etoolactivation.team_lead_check_list_5 == True and etoolactivation.spoc_check_list_1 == True and  etoolactivation.spoc_check_list_2 == True and etoolactivation.spoc_check_list_3 == True and etoolactivation.spoc_check_list_4 == True and etoolactivation.spoc_check_list_5 == True:
			etoolactivation.proceed(request.user,next_state=next_state)
			return redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))
				
		else:
			return 	redirect(reverse('admin:eToolActivation_etoolactivation_changelist'))
	except Exception as e:
		return HttpResponse(e.message)
