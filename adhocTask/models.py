from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

from river.models.fields.state import StateField
from river.models.managers.workflow_object import WorkflowObjectManager

# Create your models here.
from role.models import Role

class adhocTask(models.Model):

	task_subject = models.CharField("Task Subject",
			max_length=100,
			null=False,
			blank=False)
	task_description = models.TextField("Task Description",
			max_length=500,
			null=False,
			blank=False)
	assigned_to = models.ForeignKey(Role, 
					on_delete=models.DO_NOTHING,
					null=False, 
					blank=False,
					limit_choices_to=Q(primary_role='PL') | 
										Q(primary_role='ETSPOC') |
										Q(secondary_role='PL')|
										Q(secondary_role='ETSPOC'))
	resolution_description_history = models.CharField("Resolution Description History",
								max_length=600,
								null=True,
								blank=True)
	add_resolution_description = models.CharField("Add Resolution Description",
								max_length=200,
								null=True,
								blank=True)
	complete_restart_reason_history = models.CharField("Complete/Restart Comments History",
								max_length=600,
								null=True,
								blank=True)
	add_complete_restart_reason = models.CharField("Add Complete/Restart Comments",
								max_length=200,
								null=True,
								blank=True)
	created_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='adhoctask_create_by',
					editable=False)
	updated_by = models.ForeignKey(User, 
					on_delete=models.DO_NOTHING, 
					blank=True, 
					null=True, 
					related_name='adhoctask_update_by',
					editable=False)
	account_manager = models.CharField("Account Manager",
						max_length=20,
						null=True,
						blank=True,
						editable=False)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False)
	last_modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False)

	status = StateField(editable=False)

	objects = WorkflowObjectManager()

	def __str__(self):
		return "%s" %(self.task_subject)
