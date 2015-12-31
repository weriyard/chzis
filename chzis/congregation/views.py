from django.shortcuts import render
from django.views.generic import View
from chzis.congregation.models import Congregation


class Congregations(View):
    def get(self, request):
        congregations = Congregation.objects.only('name')
        context = dict()
        context['congregations'] = congregations
        return render(request, 'congregations.html', context)


class CongregationsMembers(View):

    def get(self, request):

        return render(request, 'congregationMembers.html', {})

