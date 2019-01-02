import datetime
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
        	'invoice_id': 123,
            'today': datetime.date.today(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        if pdf:
        	response = HttpResponse(pdf, content_type='application/pdf')
        	filename = "Invoice_%s.pdf" %("12341231")
        	content = "inline; filename='%s'" %(filename)
        	download = request.GET.get("download")
        	if download:
        		content = "attachment; filename='%s'" %(filename)
        	response['Content-Disposition'] = content
        	return response
        return HttpResponse("Report Not Found!")