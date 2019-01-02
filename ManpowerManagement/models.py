from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

# from phonenumber_field.modelfields import PhoneNumberField
from river.models.fields.state import StateField
from river.models.managers.workflow_object import WorkflowObjectManager

# Create your models here.
from role.models import Role


class EmpRegistration(models.Model):

	# etoolactivation = models.OneToOneField(
	# 					eToolActivation, 
	# 					on_delete=models.CASCADE,
	# 					related_name="eTool",
	# 					editable=False,
	# 					null=True,
	# 					blank=True)

	emp_id = models.IntegerField('Employee ID',  
				null=False, 
				blank=False,
				editable=True)
	emp_name = models.CharField("Name",
				max_length=20,
				null=False,
				blank=False)
	emp_desig = models.CharField("Designation",
					max_length=10,
					null=False,
					blank=False)
	country = models.CharField("Country",
				max_length=30,
				null=False,
				blank=False)
	branch = models.CharField("Branch",
				max_length=30,
				null=False,
				blank=False)
	office_location = models.CharField("Office Location",
						max_length=30,
						null=False,
						blank=False)
	contact_no = models.CharField("Contact No",
					max_length=15,
					null=False,
					blank=False)
	skill_set = models.CharField("Skill Set",
					max_length=50,
					null=False,
					blank=False)
	exp_yrs = models.IntegerField('Experience (Years)',  
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

	status_change_comments_history = models.CharField("Status Change Comments History",
										max_length=1000,
										null=True,
										blank=True)
	status_change_history = models.CharField("Status Change History",
								max_length=200,
								null=True,
								blank=True)
	status_change_date = models.DateField("Status Change Date",
							null=True, 
							blank=True, 
							editable=True)
	add_status_change_comments = models.CharField("Add Status Change Comments",
									max_length=200,
									null=True,
									blank=True)
	approver_comments_history = models.CharField("Record Approver Comments History",
									max_length=200,
									null=True,
									blank=True)
	add_approver_comments = models.CharField("Add Comments for Record Approver",
								max_length=1000,
								null=True,
								blank=True)
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

	class Meta:
		verbose_name = "Employee Registration"
		verbose_name_plural = "Employee Registrations"


	def __str__(self):
		return self.emp_name

	# @transaction.atomic
	# def save(self, *args, **kwargs):
	# 	# if not self.etoolactivation_id and self.status_id == 7:
	# 	# 	self.etoolactivation, _ =eToolActivation.objects.get_or_create(emp_id=self.emp_id)

	# 	if not self.account_manager:
	# 		self.account_manager =eToolActivation.objects.get_or_create(emp_id=self.emp_id)	

	# 	super(empMaster, self).save(*args, **kwargs)

