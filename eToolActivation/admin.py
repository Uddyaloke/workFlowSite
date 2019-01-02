import datetime
# from datetime import datetime

from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.
from .models import eToolActivation
# from ManpowerManagement.models import EmpRegistration
from role.models import Role

def create_river_button(obj, proceeding):
			return """
				<input
					type="button"
					style="margin:2px;2px;2px;2px;"
					value="%s"
					onclick="location.href='%s'"/>
			"""%(proceeding.meta.transition, 
				reverse('eToolActivation:proceed_eToolActivation', kwargs={'eToolActivation_id':obj.pk, 'next_state_id':proceeding.meta.transition.destination_state.pk})
				)

class eToolActivationAdmin(admin.ModelAdmin):
	
	list_display = ['emp_id', 'created_date', 'motion_date', 'completion_date', 'days_open', 'days_in_motion', 'status', 'available_actions']
	# list_filter = ["emp_id", "status"]
	search_fields = ['emp_id', 'subject', 'description']

	class Meta:
		model = eToolActivation

	def get_queryset(self, request):
		qs = super(eToolActivationAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)

		if chk_user or request.user.is_superuser:
			return qs

		elif is_spvsr:
			return qs.filter(Q(account_manager=request.user.id)|
							Q(created_by=request.user)|
							Q(updated_by=request.user))

		elif user_items:
			return qs.filter(created_by__in=user_items)

		else:
			return qs.filter(Q(created_by=request.user) |
						Q(updated_by=request.user)| 
						Q(account_manager=request.user.id))

	def get_list_display(self, request):
		self.user = request.user
		return super(eToolActivationAdmin, self).get_list_display(request)

	def completion_date(self, obj):
		completion_date = None
		eTool_qs = eToolActivation.objects.filter(id=obj.pk).values('status_id')
		if eTool_qs:
			for item in eTool_qs:
				if item['status_id'] == 5:
					completion_date = obj.last_modified_date
		return completion_date

	def days_open(self, obj):
		delta = None
		completion_date = None
		eTool_qs = eToolActivation.objects.filter(id=obj.pk).values('status_id')
		if eTool_qs:
			for item in eTool_qs:
				if item['status_id'] == 5:
					completion_date = obj.last_modified_date
		if completion_date:
			delta = completion_date - obj.created_date
		else:
			delta = timezone.now() - obj.created_date
		return delta

	def days_in_motion(self, obj):
		delta = None
		if obj.motion_date:
			completion_date = None
			eTool_qs = eToolActivation.objects.filter(id=obj.pk).values('status_id')
			if eTool_qs:
				for item in eTool_qs:
					if item['status_id'] == 5:
						completion_date = obj.last_modified_date
			if completion_date:
				delta = completion_date - obj.motion_date
			else:
				delta = timezone.now() - obj.motion_date
		return delta

	def save_model(self, request, obj, form, change): 
		if obj.created_by is None:
			obj.created_by = request.user
		obj.updated_by = request.user
		if obj.account_manager is None:
			items = Role.objects.filter(user=request.user).values('supervisor')
			for item in items:
				obj.account_manager = item['supervisor']
		obj.save()


	def available_actions(self, obj):
		content = ""
		for proceeding in obj.get_available_proceedings(self.user):
			content += create_river_button(obj, proceeding)

		return format_html(content)

	available_actions.allow_tags = True


admin.site.register(eToolActivation, eToolActivationAdmin)
