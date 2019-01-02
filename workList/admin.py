from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

# Register your models here.
from adhocTask.models import adhocTask
from ManpowerManagement.models import EmpRegistration
from eToolActivation.models import eToolActivation
from SOWRegistration.models import SOWRegistration
from role.models import Role

from .models import workList, workListByUser, workListByCategory

class workListAdmin(admin.ModelAdmin):

	list_display = ['module_name', 'items_pending_my_action', 'my_pending_action_count', 'items_pending_team_action', 'team_pending_action_count']

	class Meta:
		model = workList


	def get_queryset(self, request):
		qs = super(workListAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=request.user).values_list('id', flat=True)
		
		if chk_user or request.user.is_superuser:
			return qs

		elif is_spvsr:
			return qs
			
		elif user_items:
			if is_spoc:
				return qs.filter(mod_name__in=("eTool Activation", "Adhoc Task"))
			else:
				return qs


	def get_list_display(self, request):
		self.user = request.user
		return super(workListAdmin, self).get_list_display(request)

	def module_name(self, obj):
		return format_html("<a href='{url}'>{mod_name}</a>", url=obj.mod_url, mod_name=obj.mod_name)

	module_name.short_description = "Module Name"

	def items_pending_my_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(status_id=9))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")	

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user)|
												Q(updated_by=self.user)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		elif user_items:
			if model_name == EmpRegistration:
				wl_items = ""

			if model_name == eToolActivation:
				if is_spoc:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

				else:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14))
				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		return format_html(wl_items)

	items_pending_my_action.allow_tags=True


	def items_pending_team_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items =  model_name.objects.filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items =  model_name.objects.filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		elif user_items:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		return format_html(wl_items)

	items_pending_team_action.allow_tags=True					


	def my_pending_action_count(self, obj):
		wl_count = None
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()
			else:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

		elif is_spvsr:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=6).count()

			if model_name == eToolActivation:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()

		elif user_items:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == eToolActivation:
				if is_spoc:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4)).count()
				else:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3)).count()
			
			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14)).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19)).count()

		return wl_count

	def team_pending_action_count(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				return model_name.objects.filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(status_id=6).count()

			if model_name == eToolActivation:
				return model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"	

		elif user_items:
			if model_name == EmpRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15)).count()		
			
			if model_name == adhocTask:
				return "Not Applicable"


class workListByUserAdmin(admin.ModelAdmin):

	list_display = ['module_name', 'items_pending_my_action', 'my_pending_action_count', 'items_pending_team_action', 'team_pending_action_count']

	class Meta:
		model = workList
		

	def get_queryset(self, request):
		qs = super(workListByUserAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=request.user).values_list('id', flat=True)
		
		if chk_user or request.user.is_superuser:
			return qs

		elif is_spvsr:
			return qs
			
		elif user_items:
			if is_spoc:
				return qs.filter(mod_name__in=("eTool Activation", "Adhoc Task"))
			else:
				return qs


	def get_list_display(self, request):
		self.user = request.user
		return super(workListByUserAdmin, self).get_list_display(request)

	def module_name(self, obj):
		return format_html("<a href='{url}'>{mod_name}</a>", url=obj.mod_url, mod_name=obj.mod_name)

	module_name.short_description = "Module Name"

	def items_pending_my_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(status_id=9))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")	

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user)|
												Q(updated_by=self.user)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		elif user_items:
			if model_name == EmpRegistration:
				wl_items = ""

			if model_name == eToolActivation:
				if is_spoc:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

				else:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14))
				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		return format_html(wl_items)

	items_pending_my_action.allow_tags=True


	def items_pending_team_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items =  model_name.objects.filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items =  model_name.objects.filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		elif user_items:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		return format_html(wl_items)

	items_pending_team_action.allow_tags=True					


	def my_pending_action_count(self, obj):
		wl_count = None
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()
			else:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

		elif is_spvsr:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=6).count()

			if model_name == eToolActivation:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()

		elif user_items:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == eToolActivation:
				if is_spoc:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4)).count()
				else:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3)).count()
			
			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14)).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19)).count()

		return wl_count

	def team_pending_action_count(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				return model_name.objects.filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(status_id=6).count()

			if model_name == eToolActivation:
				return model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"	

		elif user_items:
			if model_name == EmpRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15)).count()		
			
			if model_name == adhocTask:
				return "Not Applicable"


class workListByCategoryAdmin(admin.ModelAdmin):

	list_display = ['module_name', 'items_pending_my_action', 'my_pending_action_count', 'items_pending_team_action', 'team_pending_action_count']

	class Meta:
		model = workList
		

	def get_queryset(self, request):
		qs = super(workListByCategoryAdmin, self).get_queryset(request)
		chk_user = Role.objects.filter(user=request.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=request.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=request.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=request.user).values_list('id', flat=True)
		
		if chk_user or request.user.is_superuser:
			return qs

		elif is_spvsr:
			return qs
			
		elif user_items:
			if is_spoc:
				return qs.filter(mod_name__in=("eTool Activation", "Adhoc Task"))
			else:
				return qs


	def get_list_display(self, request):
		self.user = request.user
		return super(workListByCategoryAdmin, self).get_list_display(request)

	def module_name(self, obj):
		return format_html("<a href='{url}'>{mod_name}</a>", url=obj.mod_url, mod_name=obj.mod_name)

	module_name.short_description = "Module Name"

	def items_pending_my_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(status_id=9))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")	

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user)|
												Q(updated_by=self.user)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				wl_items = ""

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(created_by=self.user).filter(status_id=18)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		elif user_items:
			if model_name == EmpRegistration:
				wl_items = ""

			if model_name == eToolActivation:
				if is_spoc:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

				else:
					items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3))
					for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14))
				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
				items = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.task_subject, loc="/admin/adhocTask/adhoctask/"+str(p.id)+"/change")		

		return format_html(wl_items)

	items_pending_my_action.allow_tags=True


	def items_pending_team_action(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		wl_items = ""

		items = ""

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items =  model_name.objects.filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items =  model_name.objects.filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		elif user_items:
			if model_name == EmpRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6)

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=str(p.emp_id) + " - " + p.emp_name, loc="/admin/ManpowerManagement/empregistration/"+str(p.id)+"/change")

			if model_name == eToolActivation:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5))

				for p in items:
						wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.subject, loc="/admin/eToolActivation/etoolactivation/"+str(p.id)+"/change")

			if model_name == SOWRegistration:
				items = model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15))

				for p in items:
					wl_items += format_html("<li><a href='{loc}'>{item_name}</a></li>",item_name=p.project_name + ", Amnd # :" + str(p.amendment_no), loc="/admin/SOWRegistration/sowregistration/"+str(p.id)+"/change")

			if model_name == adhocTask:
					wl_items = "Not Applicable"		

		return format_html(wl_items)

	items_pending_team_action.allow_tags=True					


	def my_pending_action_count(self, obj):
		wl_count = None
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)
		is_spoc = Role.objects.filter(Q(user=self.user) &
										(Q(primary_role='ETSPOC')|
										Q(secondary_role='ETSPOC')))
		role_id = Role.objects.filter(user=self.user).values_list('id', flat=True)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()
			else:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

		elif is_spvsr:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=6).count()

			if model_name == eToolActivation:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(account_manager=self.user.id)|
													Q(created_by=self.user)|
													Q(updated_by=self.user)).filter(status_id=9).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(created_by=self.user).filter(status_id=18).count()

		elif user_items:
			if model_name == EmpRegistration:
				wl_count = model_name.objects.get_object_count_waiting_for_approval(self.user)

			if model_name == eToolActivation:
				if is_spoc:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(2,4)).count()
				else:
					wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(1,3)).count()
			
			if model_name == SOWRegistration:
				wl_count = model_name.objects.filter(Q(created_by__in=user_items)|
														Q(updated_by__in=user_items)).filter(status_id__in=(10,11,12,13,14)).count()

			if model_name == adhocTask:
				wl_count = model_name.objects.filter(assigned_to_id__in=role_id).filter(status_id__in=(16,17,19)).count()

		return wl_count

	def team_pending_action_count(self, obj):
		chk_user = Role.objects.filter(user=self.user).filter(view_all=True)
		spvsr_user = Role.objects.filter(user=self.user).values_list('supervisor', flat=True)
		user_items = Role.objects.filter(supervisor__in=spvsr_user).values_list('user', flat=True)
		is_spvsr = Role.objects.filter(supervisor=self.user)

		model_name = None
		if obj.mod_name == "Employee Master":
			model_name = EmpRegistration
		if obj.mod_name == "eTool Activation":
			model_name = eToolActivation
		if obj.mod_name == "SOW Registration":
			model_name = SOWRegistration
		if obj.mod_name == "Adhoc Task":
			model_name = adhocTask

		if chk_user or self.user.is_superuser:
			if model_name == EmpRegistration:
				return model_name.objects.filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"

		elif is_spvsr:
			if model_name == EmpRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(status_id=6).count()

			if model_name == eToolActivation:
				return model_name.objects.filter(Q(account_manager=self.user.id)|
												Q(created_by=self.user.id)|
												Q(updated_by=self.user.id)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(account_manager=self.user.id).filter(~Q(status_id=15)).count()
			
			if model_name == adhocTask:
				return "Not Applicable"	

		elif user_items:
			if model_name == EmpRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(status_id=6).count()
			
			if model_name == eToolActivation:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=5)).count()
			
			if model_name == SOWRegistration:
				return model_name.objects.filter(Q(created_by__in=user_items)|Q(updated_by__in=user_items)).filter(~Q(status_id=15)).count()		
			
			if model_name == adhocTask:
				return "Not Applicable"

admin.site.register(workList, workListAdmin)

admin.site.register(workListByUser, workListByUserAdmin)

admin.site.register(workListByCategory, workListByCategoryAdmin)
