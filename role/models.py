from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Role(models.Model):
	user = models.OneToOneField(User, 
			on_delete=models.CASCADE)
	emp_id = models.CharField(max_length=10, 
				blank=True)
	primary_role = models.CharField(max_length=20, 
				blank=True,
				choices=(('PL', 'Project Lead'), 
						('AM', 'Account Manager'), 
						('ETSPOC', 'eTool SPOC'),))
	secondary_role = models.CharField(max_length=20, 
				blank=True,
				choices=(('ETSPOC', 'eTool SPOC'),))
	location = models.CharField(max_length=30, 
				blank=True)
	supervisor = models.ForeignKey(User, 
					on_delete=models.CASCADE,
					related_name="sprvsr",
					editable=True,
					null=True,
					blank=True)
	supervisor_emp_id = models.CharField(max_length=10, 
				blank=True)
	view_all = models.BooleanField("View All Recs?",
				default=False)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
	if created:
		Role.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
	instance.role.save()
