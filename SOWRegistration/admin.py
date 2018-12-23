from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from river.models import State

# Register your models here.
from role.models import Role
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

class WonCreationExtensionInstanceInline(admin.TabularInline):
    model = WonCreationExtension


class SOWRegistrationAdmin(admin.ModelAdmin):
	list_display = ['project_name', 'amnd_no', 'sow_value', 'sow_start_date', 'sow_end_date', 'owner', 'status', 'available_actions'] #'woncreationextension',
	inlines = [WonCreationExtensionInstanceInline,]
	# list_filter = ["project_name", "status"]
	search_fields = ['project_name', 'remarks']

	class Meta:
		model = SOWRegistration

	def get_queryset(self, request):
		qs = super(SOWRegistrationAdmin, self).get_queryset(request)
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

	def amnd_no(self, obj):
		return obj.amendment_no

	def get_inline_instances(self, request, obj=None):
		inline_instances = []
		inlines = []

		if obj:
			if obj.status_id and obj.status_id == 14:
				inlines = self.inlines
			else:
				inlines = []

		for inline_class in inlines:
			inline = inline_class(self.model, self.admin_site)
			if request:
				if not (inline.has_add_permission(request, obj) or
					inline.has_change_permission(request, obj) or
					inline.has_delete_permission(request, obj)):
					continue
				if not inline.has_add_permission(request, obj):
					inline.max_num = 0
			inline_instances.append(inline)
		return inline_instances

	def get_formsets(self, request, obj=None):
		for inline in self.get_inline_instances(request, obj):
			yield inline.get_formset(request, obj)

	def get_list_display(self, request):
		self.user = request.user
		return super(SOWRegistrationAdmin, self).get_list_display(request)


	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.status_id == 15:
				return [
				'project_name',
				'amendment_no', 
				'sow_value',
				'amendment_value', 
				'sow_start_date', 
				'sow_end_date',
				'amendment_start_date',
				'amendment_end_date', 
				'sow_type', 
				'owner', 
				'remarks',
				'compliance_team_approval_date',
				'tcs_contract_id',
				'legal_approval_date',
				'pob_approval',
				'pob_remarks',
				'crt_upd_won_sow'
				]
			else:
				return []
		else:
			return []


	def get_fieldsets(self, request, obj=None):
		if obj:
			if obj.status_id == 9: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks')})]
			elif obj.status_id == 10: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date')})]
			elif obj.status_id == 11: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date',
											'tcs_contract_id')})]
			elif obj.status_id == 12: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date',
											'tcs_contract_id',
											'legal_approval_date')})]
			elif obj.status_id == 13: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date',
											'tcs_contract_id',
											'legal_approval_date',
											'pob_approval',
											'pob_remarks')})]
			elif obj.status_id == 14: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date',
											'tcs_contract_id',
											'legal_approval_date',
											'pob_approval',
											'pob_remarks',
											'crt_upd_won_sow')})]
			elif obj.status_id == 15: #Open
				return [(None, {'fields': ('project_name',
											'amendment_no', 
											'sow_value',
											'amendment_value', 
											'sow_start_date', 
											'sow_end_date',
											'amendment_start_date',
											'amendment_end_date', 
											'sow_type', 
											'owner', 
											'remarks',
											'compliance_team_approval_date',
											'tcs_contract_id',
											'legal_approval_date',
											'pob_approval',
											'pob_remarks',
											'crt_upd_won_sow')})]
		else:
			return [(None, {'fields': ('project_name',
										'amendment_no', 
										'sow_value',
										'amendment_value', 
										'sow_start_date', 
										'sow_end_date',
										'amendment_start_date',
										'amendment_end_date', 
										'sow_type', 
										'owner', 
										'remarks')})]


	def get_form(self, request, obj=None, **kwargs):
		if obj:
			if obj.status_id == 9: #Open
				defaults = {'exclude': (
					'compliance_team_approval_date', 
					'tcs_contract_id',
					'legal_approval_date',
					'pob_approval',
					'pob_remarks',
					'crt_upd_won_sow',)}
			elif obj.status_id == 10: #AM Approved
				defaults = {'exclude': (
					'tcs_contract_id',
					'legal_approval_date',
					'pob_approval',
					'pob_remarks',
					'crt_upd_won_sow',)}
			elif obj.status_id == 11: #Compliance Team Approved
				defaults = {'exclude': (
					'legal_approval_date',
					'pob_approval',
					'pob_remarks',
					'crt_upd_won_sow',)}
			elif obj.status_id == 12: #CMS Uploaded
				defaults = {'exclude': (
					'pob_approval',
					'pob_remarks',
					'crt_upd_won_sow',)}
			elif obj.status_id == 13: #Legal Approved
				defaults = {'exclude': (
					'crt_upd_won_sow',)}
			elif obj.status_id == 14: #Legal Approved
				defaults = {}
			elif obj.status_id == 15: #Won Created or Updated
				defaults = {}
		else:
			defaults = {'exclude': (
					'compliance_team_approval_date', 
					'tcs_contract_id',
					'legal_approval_date',
					'pob_approval',
					'pob_remarks',
					'crt_upd_won_sow',)}

		defaults.update(kwargs)

		return super(SOWRegistrationAdmin, self).get_form(request, obj, **defaults)

	def available_actions(self, obj):
		chk_user = None
		content = ""
		items = Role.objects.filter(user=obj.created_by).values('supervisor')
		user_items = Role.objects.filter(supervisor__in=items).values_list('user', flat=True)

		for item in items:
			chk_user = item['supervisor']

		if self.user.id == chk_user or any(user_item == self.user.id for user_item in user_items):
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
		# if formset.model == SOWRegistration:
		instances = formset.save(commit=False)
		for instance in instances:
			if instance.created_by is None:
				instance.created_by = request.user
			instance.updated_by = request.user
			if instance.account_manager is None:
				items = Role.objects.filter(user=request.user).values('supervisor')
			instance.save()
		formset.save_m2m()
		# else:
		# 	formset.save()

	# def save_related(request, form, formsets, change):
	# 	if obj.created_by is None:
	# 		obj.created_by = request.user
	# 	obj.updated_by = request.user
	# 	if obj.account_manager is None:
	# 		items = Role.objects.filter(user=request.user).values('supervisor')
	# 		for item in items:
	# 			obj.account_manager = item['supervisor']
	# 	obj.save()

admin.site.register(SOWRegistration, SOWRegistrationAdmin)

class WonCreationExtensionAdmin(admin.ModelAdmin):
	list_display = ['sow_id', 'won', 'milestone', 'milestone_date', 'location', 'created_date', 'modified_date']

	class Meta:
		model = WonCreationExtension

	def get_queryset(self, request):
		qs = super(WonCreationExtensionAdmin, self).get_queryset(request)
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

	def sow_id(self, obj):
		return obj.sow_registration.tcs_contract_id

	def save_model(self, request, obj, form, change):
		if obj.created_by is None:
			obj.created_by = request.user
		obj.updated_by = request.user
		if obj.account_manager is None:
			items = Role.objects.filter(user=request.user).values('supervisor')
			for item in items:
				obj.account_manager = item['supervisor']
		obj.save()

	# def save_formset(self, request, form, formset, change): 
	# 	if formset.model == WonCreationExtension:
	# 		instances = formset.save(commit=False)
	# 		for instance in instances:
	# 			if instance.created_by is None:
	# 				instance.created_by = request.user
	# 			instance.updated_by = request.user
	# 			instance.save()
	# 	else:
	# 		formset.save()


admin.site.register(WonCreationExtension, WonCreationExtensionAdmin)
