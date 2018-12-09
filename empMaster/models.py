from __future__ import unicode_literals
import uuid

from django.conf import settings
from django.db import models

# Create your models here.


class empMaster(models.Model):
	emp_id = models.IntegerField('EMP ID',  
				null=False, 
				blank=False,
				editable=True
				)
	emp_name = models.CharField("EMP NAME",
				max_length=20,
				null=False,
				blank=False
				)
	supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, 
					on_delete=models.CASCADE,
					default=1
					)
	created_date = models.DateTimeField("Date Created",
					auto_now_add=True, 
					editable=False
					)
	modified_date = models.DateTimeField("Last Modified Date",
					auto_now=True,
					editable=False
					)


	def __str__(self):
		return self.emp_name

