from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

# Create your models here.

from empMaster.models import empMaster
from eToolActivation.models import eToolActivation
from SOWRegistration.models import SOWRegistration
from role.models import Role

class workList(models.Model):

	mod_name = models.CharField("Module Name",
				max_length=30,
				null=False,
				blank=False)
	mod_url = models.TextField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.mod_name

		
