from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

from phonenumber_field.modelfields import PhoneNumberField
from river.models.fields.state import StateField
from river.models.managers.workflow_object import WorkflowObjectManager

# Create your models here.
from role.models import Role


class empMaster(models.Model):

	# etoolactivation = models.OneToOneField(
	# 					eToolActivation, 
	# 					on_delete=models.CASCADE,
	# 					related_name="eTool",
	# 					editable=False,
	# 					null=True,
	# 					blank=True)

	emp_id = models.IntegerField('EMP ID',  
				null=False, 
				blank=False,
				editable=True)
	emp_name = models.CharField("EMP Name",
				max_length=20,
				null=False,
				blank=False)
	emp_desig = models.CharField("EMP Designation",
				max_length=10,
				null=False,
				blank=False)
	contact_no = PhoneNumberField()
	skill_set = models.CharField("Skill Set",
				max_length=50,
				null=False,
				blank=False)
	exp_yrs = models.IntegerField('Experience Years',  
				null=False, 
				blank=False,
				editable=True)
	supervisor = models.ForeignKey(Role, 
					on_delete=models.CASCADE,
					null=True, 
					blank=True,
					limit_choices_to=Q(primary_role='PL') | 
										Q(primary_role='AM') |
										Q(secondary_role='PL'))
	account_manager = models.CharField("Account Manager",
						max_length=20,
						null=True,
						blank=True,
						editable=False)
	onboard_date = models.DateField("Onboard Date",
					null=True, 
					blank=True, 
					editable=True)
	cswon =  models.CharField("CSWON",
				max_length=20,
				null=True,
				blank=True)
	created_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='create_by',
					editable=False)
	updated_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='update_by',
					editable=False)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False)
	modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False)

	status = StateField(editable=False)

	objects = WorkflowObjectManager()

	def __str__(self):
		return self.emp_name

	# @transaction.atomic
	# def save(self, *args, **kwargs):
	# 	# if not self.etoolactivation_id and self.status_id == 7:
	# 	# 	self.etoolactivation, _ =eToolActivation.objects.get_or_create(emp_id=self.emp_id)

	# 	if not self.account_manager:
	# 		self.account_manager =eToolActivation.objects.get_or_create(emp_id=self.emp_id)	

	# 	super(empMaster, self).save(*args, **kwargs)

