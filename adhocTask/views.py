from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now


from river.models import State

# Create your views here.
from .models import adhocTask


def proceed_adhocTask(request, adhocTask_id, next_state_id=None):
	adhoctask = get_object_or_404(adhocTask, pk=adhocTask_id)
	next_state = get_object_or_404(State, pk=next_state_id)
	adhoctask.updated_by = request.user

	try:
		if adhoctask.status_id == 17:
			if adhoctask.resolution_description_history:
				adhoctask.proceed(request.user,next_state=next_state)
				messages.success(request, 'Proceed Action Completed Successfully')
				return redirect(reverse('admin:adhocTask_adhoctask_changelist'))
			else:
				messages.error(request, 'Cannot Proceed. Please Check if Resolution Description is Provided?')
				return 	redirect(reverse('admin:adhocTask_adhoctask_changelist'))

		elif adhoctask.status_id == 18:
			if adhoctask.complete_restart_reason_history:
				adhoctask.proceed(request.user,next_state=next_state)
				messages.success(request, 'Proceed Action Completed Successfully')
				return redirect(reverse('admin:adhocTask_adhoctask_changelist'))
			else:
				messages.error(request, 'Cannot Proceed. Please Check if Complete/Restart Comments are Provided?')
				return redirect(reverse('admin:adhocTask_adhoctask_changelist'))

		else:
			adhoctask.proceed(request.user,next_state=next_state)
			messages.success(request, 'Proceed Action Completed Successfully')
			return redirect(reverse('admin:adhocTask_adhoctask_changelist'))
				
	except Exception as e:
		return HttpResponse("Error {0}".format(str(e.args[0])).encode("utf-8"))
