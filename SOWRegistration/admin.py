from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from river.models import State

# Register your models here.
from .models import SOWRegistration, WonCreationExtension

def create_river_button(obj, proceeding):
			return """
				<input
					type="button"
					style="margin:2px;2px;2px;2px;"
					value="%s"
					onclick="location.href='%s'"/>
			"""%(proceeding.meta.transition, 
				reverse('SOWRegistration:proceed_SOWRegistration', kwargs={'SOWRegistration_id':obj.pk, 'next_state_id':proceeding.meta.transition.destination_state.pk})
				)

class SOWRegistrationAdmin(admin.ModelAdmin):
	list_display = ['project_name', 'sow_value', 'sow_start_date', 'sow_end_date', 'owner', 'created_date', 'modified_date',  'status', 'available_actions'] #'woncreationextension',

	class Meta:
		model = SOWRegistration

	def get_list_display(self, request):
		self.user = request.user
		return super(SOWRegistrationAdmin, self).get_list_display(request)

	# def etool_activation(self, obj):
	# 	eTool = None
	# 	eTool_qs = eToolActivation.objects.filter(emp_id=obj.emp_id).values('status_id')
	# 	if eTool_qs:
	# 		state_qs = State.objects.filter(id__in=eTool_qs).values('label')
	# 		for item in state_qs:
	# 			eTool = item['label']
	# 		return eTool
	# 	else:
	# 		return None

	def available_actions(self, obj):
		content = ""
		for proceeding in obj.get_available_proceedings(self.user):
			content += create_river_button(obj, proceeding)

		return format_html(content)

	available_actions.allow_tags = True

admin.site.register(SOWRegistration, SOWRegistrationAdmin)

class WonCreationExtensionAdmin(admin.ModelAdmin):
	list_display = ['tcs_contract_id', 'won', 'start_date', 'end_date', 'location', 'created_date', 'modified_date']

	class Meta:
		model = WonCreationExtension

	# def get_list_display(self, request):
	# 	self.user = request.user
	# 	return super(WonCreationExtension, self).get_list_display(request)

admin.site.register(WonCreationExtension, WonCreationExtensionAdmin)
