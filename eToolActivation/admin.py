from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import eToolActivation

def create_river_button(obj, proceeding):
			return """
				<input
					type="button"
					style="margin:2px;2px;2px;2px;"
					value="%s"
					onclick="location.href='%s'"/>
			"""%(proceeding.meta.transition, 
				reverse('eToolActivation:proceed_eToolActivation', kwargs={'eToolActivation_id':obj.pk, 'next_state_id':proceeding.meta.transition.destination_state.pk})
				)

class eToolActivationAdmin(admin.ModelAdmin):
	list_display = ['no', 'subject', 'description', 'status', 'river_actions']

	def get_list_display(self, request):
		self.user = request.user
		return super(eToolActivationAdmin, self).get_list_display(request)


	def river_actions(self, obj):
		content = ""
		for proceeding in obj.get_available_proceedings(self.user):
			content += create_river_button(obj, proceeding)

		return format_html(content)

	river_actions.allow_tags = True


admin.site.register(eToolActivation, eToolActivationAdmin)
