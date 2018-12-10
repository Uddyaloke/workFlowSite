from __future__ import unicode_literals
import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from river.models.fields.state import StateField

# Create your models here.

class eToolActivation(models.Model):

	# emp_master = models.ForeignKey(
	# 				empMaster, 
	# 				on_delete=models.CASCADE
	# 				)
	emp_id = models.IntegerField("EMP ID",
				null=False,
				blank=False,
				editable=False)
	no = models.CharField("Item Number", 
			max_length=50, 
			default=uuid.uuid4, 
			null=False, 
			blank=False,
			editable=False)
	subject = models.CharField("Subject",
			max_length=100,
			null=False,
			blank=False)
	description = models.TextField("Item Description",
			max_length=500,
			null=True,
			blank=True)
	team_lead_check_list_1 = models.BooleanField("Team Lead Check List 1", 
					default=False)
	team_lead_check_list_2 = models.BooleanField("Team Lead Check List 2", 
					default=False)
	team_lead_check_list_3 = models.BooleanField("Team Lead Check List 3", 
					default=False)
	team_lead_check_list_4 = models.BooleanField("Team Lead Check List 4", 
					default=False)
	team_lead_check_list_5 = models.BooleanField("Team Lead Check List 5", 
					default=False)
	team_lead_comments = models.TextField("Team Lead Comments",
			max_length=200,
			null=True,
			blank=True)
	spoc_check_list_1 = models.BooleanField("SPOC Check List 1", 
					default=False)
	spoc_check_list_2 = models.BooleanField("SPOC Check List 2", 
					default=False)
	spoc_check_list_3 = models.BooleanField("SPOC Check List 3", 
					default=False)
	spoc_check_list_4 = models.BooleanField("SPOC Check List 4", 
					default=False)
	spoc_check_list_5 = models.BooleanField("SPOC Check List 5", 
					default=False)
	spoc_comments = models.TextField("SPOC Comments",
			max_length=200,
			null=True,
			blank=True)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False
					)
	last_modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False
					)
	motion_date = models.DateTimeField("Motion Date",
						default=None, 
						null=True, 
						blank=True,
						editable=False
						)

	status = StateField(editable=False)

	def __str__(self):
		return "%s" %(self.status)


def pre_save_post_motion_receiver(sender, instance, *args, **kwargs):
	if instance.status_id == 2 and instance.motion_date is None:
		instance.motion_date = timezone.now()

pre_save.connect(pre_save_post_motion_receiver, sender=eToolActivation)

