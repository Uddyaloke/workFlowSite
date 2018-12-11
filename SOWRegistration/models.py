from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import pre_save
from django.utils import timezone

from river.models.fields.state import StateField

# Create your models here.

class WonCreationExtension(models.Model):

	tcs_contract_id = models.CharField("TCS Contract ID",
						max_length=50,
						null=False,
						blank=False,
						editable=False)
	won = models.CharField("WON",
			max_length=10,
			null=False,
			blank=False,
			editable=False)
	start_date = models.DateField("Start Date",
					null=False, 
					blank=False,
					editable=True)
	end_date = models.DateField("End Date",
					null=False, 
					blank=False,
					editable=True)
	location = models.CharField("Location",
			max_length=50,
			null=True,
			blank=True,
			editable=True)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False
					)
	modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False
					)


class SOWRegistration(models.Model):

	project_name = models.CharField("Project Name",
					max_length=50,
					null=False,
					blank=False,
					editable=True)
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
	sow_type = models.CharField("Type",
				max_length=10,
				null=False,
				blank=False,
				editable=True)
	owner = models.ForeignKey(User, 
				on_delete=models.DO_NOTHING, 
				blank=False, 
				null=False, 
				related_name='create')
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
	woncreationextension = models.OneToOneField(
							WonCreationExtension, 
							on_delete=models.CASCADE,
							related_name="woncrtext",
							editable=False,
							null=True,
							blank=True,)
	won = models.CharField("WON",
			max_length=10,
			null=True,
			blank=True,
			editable=True)
	location = models.CharField("Location",
			max_length=50,
			null=True,
			blank=True,
			editable=True)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False
					)
	modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False
					)

	status = StateField(editable=False)

	def __str__(self):
		return "%s" %(self.project_name)

	@transaction.atomic
	def save(self, *args, **kwargs):
		if not self.woncreationextension_id and self.status_id == 15:
			self.woncreationextension, _ =WonCreationExtension.objects.update_or_create(
											tcs_contract_id=self.tcs_contract_id,
											won=self.won,
											defaults={
												"location": self.location,
												"start_date": self.sow_start_date,
												"end_date": self.sow_end_date
											})

		elif self.woncreationextension_id and self.status_id == 15:
			self.woncreationextension, _ =WonCreationExtension.objects.update_or_create(
											tcs_contract_id=self.tcs_contract_id,
											won=self.won,
											defaults={
												"location": self.location,
												"start_date": self.sow_start_date,
												"end_date": self.sow_end_date
											})

		super(SOWRegistration, self).save(*args, **kwargs)





