import datetime
# from datetime import datetime

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.
from .models import eToolActivation
from empMaster.models import empMaster

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

	def get_list_display(self, request):
		self.user = request.user
		return super(eToolActivationAdmin, self).get_list_display(request)

	# def emp_id(self, obj):
	# 	return obj.emp_master.emp_id

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


	def available_actions(self, obj):
		content = ""
		for proceeding in obj.get_available_proceedings(self.user):
			content += create_river_button(obj, proceeding)

		return format_html(content)

	available_actions.allow_tags = True


admin.site.register(eToolActivation, eToolActivationAdmin)
