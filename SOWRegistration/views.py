from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import SOWRegistration

def proceed_SOWRegistration(request, SOWRegistration_id, next_state_id=None):
	sowregistration = get_object_or_404(SOWRegistration, pk=SOWRegistration_id)
	next_state = get_object_or_404(State, pk=next_state_id)

	try:
		if sowregistration.status_id == 9:
			sowregistration.proceed(request.user,next_state=next_state)
			return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))

		elif sowregistration.status_id == 10:
			if sowregistration.compliance_team_approval_date is not None:
				sowregistration.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))
			else:
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))

		elif sowregistration.status_id == 11:
			if sowregistration.tcs_contract_id is not None:
				sowregistration.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))
			else:
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))

		elif sowregistration.status_id == 12:
			if sowregistration.legal_approval_date is not None:
				sowregistration.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))
			else:
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))

		elif sowregistration.status_id == 13:
			if sowregistration.pob_approval == True and sowregistration.pob_remarks is not None:
				sowregistration.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))
			else:
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))

		elif sowregistration.status_id == 14:
			if sowregistration.won is not None and sowregistration.location is not None:
				sowregistration.proceed(request.user,next_state=next_state)
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))
			else:
				return redirect(reverse('admin:SOWRegistration_sowregistration_changelist'))		

	except Exception as e:
		return HttpResponse(e.message)
