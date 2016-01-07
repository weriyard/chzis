from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from chzis.congregation.models import Congregation, CongregationMember


class Congregations(View):
    def get(self, request):
        default_congregation = request.user.profile.default_congregation
        if default_congregation is not None and not 'menu' in request.GET:
            return redirect('/congregation/{}/'.format(default_congregation.id))
        congregations = Congregation.objects.only('name')
        context = dict()
        context['congregations'] = congregations
        return render(request, 'congregations.html', context)

    def post(self, request):
        print request.POST
        if 'default' in request.POST and int(request.POST.get('default')) != request.user.profile.default_congregation.id:
            profile = request.user.profile
            congregation = Congregation.objects.get(id=request.POST.get('default'))
            profile.default_congregation = congregation
            profile.save()
        return redirect("{}?menu=1".format(request.path))



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

    def post(self, request, congregation_id, member_id):
        cong_member = CongregationMember.objects.get(id=member_id)

        for field in CongregationMember._meta.fields:
            if field.name in ['id', 'owner', 'user', 'congregation',
                              'last_modification', 'baptism_date', 'age', 'coordinator', 'active']:
                continue
            setattr(cong_member, field.name, bool(request.POST.get(field.name, False)))

        cong_member.save()
        return redirect(request.path)
