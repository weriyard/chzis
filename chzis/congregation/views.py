from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from chzis.congregation.models import Congregation, CongregationMember


class Congregations(View):
    def get(self, request):
        default_congregation = request.user.profile.default_congregation
        if default_congregation is not None and not 'menu' in request.GET:
            return redirect('/congregations/{}/'.format(default_congregation.id))
        congregations = Congregation.objects.only('name')
        context = dict()
        context['congregations'] = congregations
        return render(request, 'congregations.html', context)

    def post(self, request):
        if 'default' in request.POST:
            profile = request.user.profile
            congregation = Congregation.objects.get(id=request.POST.get('default'))
            profile.default_congregation = congregation
            profile.save()
        return redirect("{}".format(request.path))


class CongregationDetails(TemplateView):
    template_name = "congregationDetails.html"

    def get_context_data(self, congregation_id):
        cong_members = CongregationMember.objects.filter(congregation_id=congregation_id)
        context = dict()
        context['cong_members'] = cong_members
        return context


class CongregationMemberDetails(TemplateView):
    template_name = "congregationMember.html"

    def get_context_data(self, congregation_id, member_id):
        member = CongregationMember.objects.get(id=member_id)

        context = dict()
        context['member'] = member
        return context


    def post(self, request, congregation_id, member_id):
        print "VALE POSTAAA"
        cong_member = CongregationMember.objects.get(id=member_id)

        for field in CongregationMember._meta.fields:
            if field.name in ['id', 'owner', 'user', 'congregation',
                              'last_modification', 'baptism_date', 'age', 'coordinator', 'active']:
                continue
            setattr(cong_member, field.name, bool(request.POST.get(field.name, False)))

        cong_member.save()
        return redirect(request.path)
