from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import EmpRegistration
from eToolActivation.models import eToolActivation

def proceed_EmpRegistration(request, EmpRegistration_id, next_state_id=None):
	empregistration = get_object_or_404(EmpRegistration, pk=EmpRegistration_id)
	next_state = get_object_or_404(State, pk=next_state_id)
	current_state = get_object_or_404(State, pk=empregistration.status_id)
	status_change_string = current_state.label + '-->' + next_state.label
	# etoolactivation = eToolActivation.objects.filter(emp_master_id=empMaster_id)
	etoolactivation = eToolActivation.objects.filter(emp_id=empregistration.emp_id)

	try:
		if empregistration.status_id == 1:
			initial_data =''
			if empregistration.status_change_date and empregistration.approver_comments_history:
				empregistration.proceed(request.user,next_state=next_state)

				if empregistration.status_change_history:
					initial_data = empregistration.status_change_history
				empregistration.status_change_history = initial_data + str(empregistration.status_change_date) + '| ' + status_change_string + '\n'

				empregistration.updated_by = request.user
				empregistration.status_change_date = ''
				empregistration.save()
				messages.success(request, 'Proceed Action Completed Successfully')
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))
			else:
				messages.error(request, 'Cannot Proceed. Please Check if Status Change Date/Comments are Provided?')
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))

		elif next_state_id and next_state_id != 12:
			initial_data =''
			if empregistration.status_change_date and empregistration.status_change_comments_history:
				empregistration.proceed(request.user,next_state=next_state)

				if empregistration.status_change_history:
					initial_data = empregistration.status_change_history
				empregistration.status_change_history = initial_data + str(empregistration.status_change_date) + '| ' + status_change_string + '\n'

				empregistration.updated_by = request.user
				empregistration.status_change_date = ''
				empregistration.save()
				messages.success(request, 'Proceed Action Completed Successfully')
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))
			else:
				messages.error(request, 'Cannot Proceed. Please Check if Status Change Date/Comments are Provided?')
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))

		elif next_state_id and next_state_id == 12:
			initial_data =''
			if empregistration.status_change_date and empregistration.status_change_comments_history and empregistration.onboard_date:
				empregistration.proceed(request.user,next_state=next_state)

				if empregistration.status_change_history:
					initial_data = empregistration.status_change_history
				empregistration.status_change_history = initial_data + str(empregistration.status_change_date) + '| ' + status_change_string + '\n'

				empregistration.updated_by = request.user
				empregistration.status_change_date = ''
				empregistration.save()
				messages.success(request, 'Proceed Action Completed Successfully')
				if not etoolactivation and empregistration.status_id == 12:
					eToolActivation.objects.create(emp_id=empregistration.emp_id, subject='eTool Activation of ' + str(empregistration.emp_id) + ' - ' + empregistration.emp_name, created_by=empregistration.created_by, updated_by=empregistration.updated_by, account_manager=empregistration.account_manager)	
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))
			else:
				messages.error(request, 'Cannot Proceed. Please Check if Status Change Date/Comments/On-board Date are Provided?')
				return redirect(reverse('admin:ManpowerManagement_empregistration_changelist'))		

	except Exception as e:
		return HttpResponse(e.messages)
