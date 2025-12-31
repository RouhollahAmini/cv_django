from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

class ContactView(TemplateView):
    template_name = 'contact/contact.html'

class SendMessageView(TemplateView):
    def post(self, request):
        return JsonResponse({'success': True})