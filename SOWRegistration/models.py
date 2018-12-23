from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models , transaction
from django.db.models import ExpressionWrapper, F, Q
from django.db.models.signals import post_save

# from django.db.models.signals import pre_save
# from django.utils import timezone

from river.models.fields.state import StateField
from river.models.managers.workflow_object import WorkflowObjectManager

# Create your models here.
from role.models import Role

class SOWRegistration(models.Model):

	project_name = models.CharField("Project Name",
					max_length=50,
					null=False,
					blank=False,
					editable=True)
	amendment_no = models.PositiveSmallIntegerField("Amendment Number",
					null=False,
					blank=False,
					default=0)
	sow_value = models.DecimalField("SOW Value",
					max_digits=10, 
					decimal_places=2,
					null=False, 
					blank=False,
					editable=True)
	sow_start_date = models.DateField("SOW Start Date",
						null=False, 
						blank=False,
						editable=True)
	sow_end_date = models.DateField("SOW End Date",
					null=False, 
					blank=False,
					editable=True)
	amendment_value = models.DecimalField("Amendment Value",
						max_digits=10, 
						decimal_places=2,
						null=True, 
						blank=True,
						editable=True)
	amendment_start_date = models.DateField("Amendment Start Date",
							null=True, 
							blank=True,
							editable=True)
	amendment_end_date = models.DateField("Amendment End Date",
							null=True, 
							blank=True,
							editable=True)
	sow_type = models.CharField("Type",
				max_length=10,
				null=False,
				blank=False,
				editable=True)
	owner = models.ForeignKey(Role, 
					on_delete=models.DO_NOTHING,
					null=True, 
					blank=True,
					limit_choices_to=Q(primary_role='AM'))
	remarks = models.TextField("Remarks",
				max_length=200,
				null=True,
				blank=True,
				editable=True)
	compliance_team_approval_date = models.DateField("Compliance Team Approval Date",
										null=True, 
										blank=True,
										editable=True)
	tcs_contract_id = models.CharField("TCS Contract ID",
						max_length=50,
						null=True,
						blank=True,
						editable=True)
	legal_approval_date = models.DateField("Legal Approval Date",
							null=True, 
							blank=True,
							editable=True)
	pob_approval = models.BooleanField("POB Approval", 
					default=False)
	pob_remarks = models.CharField("POB Remarks",
						max_length=200,
						null=True,
						blank=True,
						editable=True)
	crt_upd_won_sow = models.BooleanField("Create/Update WONs for SOW ID", 
						default=False)
	account_manager = models.CharField("Account Manager",
						max_length=20,
						null=True,
						blank=True,
						editable=False)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False)
	modified_date = models.DateTimeField("Last Modified Date",
						auto_now=True,
						editable=False)
	created_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='sowreg_create_by',
					editable=False)
	updated_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='sowreg_update_by',
					editable=False)

	status = StateField(editable=False)

	objects = WorkflowObjectManager()

	def __str__(self):
		return "%s" %(self.project_name)


	@transaction.atomic
	def save(self, *args, **kwargs):
		if not self.amendment_start_date and self.amendment_no == 0:
			self.amendment_start_date = self.sow_start_date

		if not self.amendment_end_date and self.amendment_no == 0:
			self.amendment_end_date = self.sow_end_date

		super(SOWRegistration, self).save(*args, **kwargs)

# def my_callback(sender, instance, created, **kwargs):
# 	if created:
# 		sowregistration = instance
# 		if sowregistration.project_name == self.project_name:
# 			sowregistration.amendment_no = F('amendment_no') + 1
# 			sowregistration.save(update_fields='amendment_no') # save the counter field only

# post_save.connect(my_callback, sender=SOWRegistration)


class WonCreationExtension(models.Model):

	sow_registration = models.ForeignKey(
						SOWRegistration, 
						on_delete=models.DO_NOTHING,
						related_name="sowregn",
						editable=True,
						null=True,
						blank=True)
	won = models.CharField("WON",
			max_length=10,
			null=True,
			blank=True,
			editable=True)
	milestone = models.DecimalField("Milestone",
					max_digits=10, 
					decimal_places=2,
					null=True, 
					blank=True,
					editable=True)
	milestone_date = models.DateField("Milestone Date",
					null=True, 
					blank=True,
					editable=True)
	location = models.CharField("Location",
				max_length=50,
				null=True,
				blank=True,
				editable=True)
	account_manager = models.CharField("Account Manager",
						max_length=20,
						null=True,
						blank=True,
						editable=False)
	created_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='won_create_by',
					editable=False)
	updated_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='won_update_by',
					editable=False)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False)
	modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False)

	def __str__(self):
		return "%s -- %s" %(self.sow_registration, self.sow_registration.tcs_contract_id)


	# @transaction.atomic
	# def save(self):
	# 	if not self.id:
	# 		self.tcs_contract_id = sowregistration.tcs_contract_id
	# 	super(WonCreationExtension, self).save()

	# @transaction.atomic
	# def save(self, *args, **kwargs):
	# 	obj = WonCreationExtension.objects.filter(SOWRegistration_id=self.id)
	# 	if not self.woncreationextension_id and self.status_id == 15:
	# 		self.woncreationextension, _ =WonCreationExtension.objects.get_or_create(
	# 										tcs_contract_id=self.tcs_contract_id,
	# 										# won=self.won,
	# 										defaults={
	# 											"won": None,
	# 											"location": None,
	# 											"milestone": None,
	# 											"milestone_date": None
	# 										})

	# 	super(SOWRegistration, self).save(*args, **kwargs)

