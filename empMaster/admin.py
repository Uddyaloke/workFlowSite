from django.contrib import admin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from river.models import State

# Register your models here.
from eToolActivation.models import eToolActivation
from role.models import Role
from .models import empMaster

def create_river_button(obj, proceeding):
			return """
				<input
					type="button"
					style="margin:2px;2px;2px;2px;"
					value="%s"
					onclick="location.href='%s'"/>
			"""%(proceeding.meta.transition, 
				reverse('empMaster:proceed_empMaster', kwargs={'empMaster_id':obj.pk, 'next_state_id':proceeding.meta.transition.destination_state.pk})
				)

class empMasterAdmin(admin.ModelAdmin):
	list_display = ['emp_id', 'emp_name', 'skill_set', 'contact_no', 'supervisor', 'onboard_date', 'etool_activation', 'status', 'available_actions']
	# list_filter = ["emp_id", "status"]
	search_fields = ['emp_id', 'emp_name', 'emp_desig', 'skill_set']

	class Meta:
		model = empMaster

	def get_queryset(self, request):
		qs = super(empMasterAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)
		
		if chk_user or request.user.is_superuser:
			return qs

		elif is_spvsr:
			return qs.filter(account_manager=request.user.id)
			
		elif user_items:
			return qs.filter(created_by__in=user_items)
			
		else:
			return qs.filter(Q(created_by=request.user) |
						Q(updated_by=request.user)| 
						Q(account_manager=request.user.id))					

	def get_list_display(self, request):
		self.user = request.user
		return super(empMasterAdmin, self).get_list_display(request)

	def etool_activation(self, obj):
		eTool = None
		eTool_qs = eToolActivation.objects.filter(emp_id=obj.emp_id).values('status_id')
		if eTool_qs:
			state_qs = State.objects.filter(id__in=eTool_qs).values('label')
			for item in state_qs:
				eTool = item['label']
			return eTool
		else:
			return None

	def available_actions(self, obj):
		chk_user = None
		content = ""
		items = Role.objects.filter(user=obj.created_by).values('supervisor')
		for item in items:
			chk_user = item['supervisor']
		# if not self.user == obj.created_by or self.user.id == chk_user:
		if self.user.id == chk_user:
			for proceeding in obj.get_available_proceedings(self.user):
				content += create_river_button(obj, proceeding)

		return format_html(content)

	available_actions.allow_tags = True

	def save_model(self, request, obj, form, change):
		if obj.created_by is None:
			obj.created_by = request.user
		obj.updated_by = request.user
		if obj.account_manager is None:
			items = Role.objects.filter(user=request.user).values('supervisor')
			for item in items:
				obj.account_manager = item['supervisor']
		obj.save()

	def save_formset(self, request, form, formset, change): 
		if formset.model == empMaster:
			instances = formset.save(commit=False)
			for instance in instances:
				if instance.created_by is None:
					instance.created_by = request.user
				instance.updated_by = request.user
				instance.save()
		else:
			formset.save()

admin.site.register(empMaster, empMasterAdmin)
