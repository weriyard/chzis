from django.shortcuts import render
from django.views.generic import View


class CongregationsMembers(View):

    def get(self, request):
        return render(request, 'congregationMembers.html', {})

