from django.shortcuts import render
from django.views.generic import View
from django.views.generic import ListView
from chzis.congregation.models import Congregation, CongregationMember

class Congregations(View):
    def get(self, request):
        default_congregation = request.user.profile.default_congregation
        if default_congregation is not None:
            return #redirect to konkretna kongregacja
        congregations = Congregation.objects.only('name')
        context = dict()
        context['congregations'] = congregations
        return render(request, 'congregations.html', context)


class CongregationDetails(View):

    def get(self, request, congregation_id):
        cong_members = CongregationMember.objects.filter(congregation_id=congregation_id)

        context = dict()
        context['cong_members'] = cong_members
        return render(request, 'congregationDetails.html', context)


class CongregationMemberDetails(View):

    def get(self, request, congregation_id, member_id):
        member = CongregationMember.objects.get(id=member_id)

        context = dict()
        context['member'] = member
        return render(request, 'congregationMember.html', context)
