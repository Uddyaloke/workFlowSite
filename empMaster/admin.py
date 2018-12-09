from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from river.models import State

# Register your models here.
from eToolActivation.models import eToolActivation
from .models import empMaster

class empMasterAdmin(admin.ModelAdmin):
	list_display = ['emp_id', 'emp_name', 'supervisor', 'created_date', 'modified_date', 'etool_activation']

	class Meta:
		model = empMaster

	def get_list_display(self, request):
		self.user = request.user
		return super(empMasterAdmin, self).get_list_display(request)

	def etool_activation(self, obj):
		eTool = None
		eTool_qs = eToolActivation.objects.filter(emp_master_id=obj.pk).values('status_id')
		if eTool_qs:
			state_qs = State.objects.filter(id__in=eTool_qs).values('label')
			for item in state_qs:
				eTool = item['label']
			return eTool
		else:
			return None

admin.site.register(empMaster, empMasterAdmin)
