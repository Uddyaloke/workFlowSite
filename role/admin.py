from django.contrib import admin

# Register your models here.
from .models import Role


class RoleAdmin(admin.ModelAdmin):
	list_display = ['user', 'emp_id', 'primary_role', 'secondary_role', 'location', 'supervisor', 'supervisor_emp_id']

	class Meta:
		model = Role

	def get_list_display(self, request):
		self.user = request.user
		return super(RoleAdmin, self).get_list_display(request)


admin.site.register(Role, RoleAdmin)
