import datetime
import re
# from datetime import datetime

from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.
from .models import adhocTask
from role.models import Role


class adhocTaskAdmin(admin.ModelAdmin):
	
	list_display = ['task_subject', 'assigned_to', 'created_date', 'days_open', 'completion_date', 'status', 'available_actions']
	search_fields = ["task_subject", "task_description", "resolution_description", "complete_restart_reason", ]

	class Meta:
		model = adhocTask

	def get_queryset(self, request):
		qs = super(adhocTaskAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)
		role_id = Role.objects.filter(user=request.user).values_list('id', flat=True)

		if chk_user:
			return qs.filter(created_by=request.user)

		elif is_spvsr:
			return qs.filter(Q(created_by=request.user)|
							Q(assigned_to_id__in=role_id))

		elif user_items:
			return qs.filter(assigned_to_id__in=role_id)

		else:
			return qs

	def get_list_display(self, request):
		self.user = request.user
		return super(adhocTaskAdmin, self).get_list_display(request)

	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.status_id > 16 and request.user == obj.created_by:
				return [
					'task_subject',
					'task_description', 
					'assigned_to',
					'resolution_description_history',
					'add_resolution_description', 
					'complete_restart_reason_history'
					]
			elif obj.status_id > 16:
				return [
					'task_subject',
					'task_description', 
					'assigned_to',
					'resolution_description_history', 
					'complete_restart_reason_history',
					'add_complete_restart_reason'
					]
			else:
				return [
					'task_subject',
					'task_description', 
					'assigned_to',
					'resolution_description_history',
					'add_resolution_description', 
					'complete_restart_reason_history',
					'add_complete_restart_reason'
					]
		else:
			return [
				'resolution_description_history',
				'add_resolution_description', 
				'complete_restart_reason_history',
				'add_complete_restart_reason'
				]


	def get_fieldsets(self, request, obj=None):
		if obj:
			if obj.status_id == 16:
				if request.user == obj.created_by:
					return [(None, {'fields': ('task_subject',
												'task_description', 
												'assigned_to')})]
				else:
					return [(None, {'fields': ('task_subject',
												'task_description')})]

			if obj.status_id == 17:
				return [(None, {'fields': ('task_subject',
											'task_description', 
											'assigned_to',
											'resolution_description_history',
											'add_resolution_description')})]
			if obj.status_id > 17:
				return [(None, {'fields': ('task_subject',
											'task_description', 
											'assigned_to',
											'resolution_description_history',
											'add_resolution_description',
											'complete_restart_reason_history',
											'add_complete_restart_reason')})]

		else:
			return [(None, {'fields': ('task_subject',
										'task_description', 
										'assigned_to')})]


	def completion_date(self, obj):
		completion_date = None
		adhoctask_qs = adhocTask.objects.filter(id=obj.pk).values('status_id')
		if adhoctask_qs:
			for item in adhoctask_qs:
				if item['status_id'] == 20:
					completion_date = obj.last_modified_date
		return completion_date

	def days_open(self, obj):
		delta = None
		completion_date = None
		adhoctask_qs = adhocTask.objects.filter(id=obj.pk).values('status_id')
		if adhoctask_qs:
			for item in adhoctask_qs:
				if item['status_id'] == 20:
					completion_date = obj.last_modified_date
		if completion_date:
			delta = completion_date - obj.created_date
		else:
			delta = timezone.now() - obj.created_date
		return delta


	def save_model(self, request, obj, form, change): 
		now = datetime.datetime.now()

		if obj.created_by is None:
			obj.created_by = request.user

		obj.updated_by = request.user

		if obj.account_manager is None:
			items = Role.objects.filter(user=request.user).values('supervisor')

			for item in items:
				obj.account_manager = item['supervisor']

		obj.add_resolution_description = ''

		obj.add_complete_restart_reason = ''

		if request.POST.get('add_resolution_description'):
			initial_data = ''

			if obj.resolution_description_history:
				initial_data = obj.resolution_description_history

			obj.resolution_description_history = initial_data + now.strftime("%Y-%m-%d %H:%M") + '| ' + request.POST.get('add_resolution_description') + '\n'

		if request.POST.get('add_complete_restart_reason'):
			initial_data = ''

			if obj.complete_restart_reason_history:
				initial_data = obj.complete_restart_reason_history

			obj.complete_restart_reason_history = initial_data + now.strftime("%Y-%m-%d %H:%M") + '| ' + request.POST.get('add_complete_restart_reason') + '\n'	

		obj.save()

	def available_actions(self, obj):
		
		final_cnt = obj.get_available_proceedings(self.user).count()

		if final_cnt and final_cnt > 0:

			content = f"<select id='proceed-action-select-%s'>\
					<option value=''>------------------------------------</option></br>"%(obj.pk)

			for proceeding in obj.get_available_proceedings(self.user):
				content += f"<option value='%s'>%s</option>"%(reverse('adhocTask:proceed_adhocTask', kwargs={'adhocTask_id':obj.pk, 'next_state_id':proceeding.meta.transition.destination_state.pk}), proceeding.meta.transition)
			
			content += f"</select>\
						<button id='proceed-action' type='submit' class='button btn-ok' onclick='myFunction(event, %s)'>Proceed</button>"%(obj.pk)

			return format_html(content)

	available_actions.allow_tags = True

admin.site.register(adhocTask, adhocTaskAdmin)
