from django.shortcuts import render
from django.views.generic import View, TemplateView, RedirectView
from django.shortcuts import redirect
from chzis.congregation.models import Congregation, CongregationMember
from django.core import exceptions


class CongregationRedirect(RedirectView):
    url = ""

    def get_redirect_url(self, *args, **kwargs):
        default_congregation = self.request.user.profile.default_congregation
        if default_congregation is not None:
            redirect_url = '/congregations/{}/'.format(default_congregation.id)
        else:
            redirect_url = '/congregations/all/'
        return self.url + redirect_url


class Congregations(TemplateView):
    template_name = 'congregations.html'

    def get_context_data(self):
        congregations = Congregation.objects.only('name')
        context = dict()
        context['congregations'] = congregations
        return context

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

    def get_context_data(self, member_id, *args, **kwargs):
        if 'congregation_id' in kwargs:
            member = CongregationMember.objects.get(congregation__id=kwargs.get('congregation_id'), user__id=member_id)
        else:
            try:
                member = CongregationMember.objects.get(user__id=member_id)
            except exceptions.ObjectDoesNotExist:
                member = None

        context = dict()
        context['member'] = member
        return context

    def post(self, request, congregation_id, member_id):
        cong_member = CongregationMember.objects.get(id=member_id)

        for field in CongregationMember._meta.fields:
            if field.name in ['id', 'owner', 'user', 'congregation',
                              'last_modification', 'baptism_date', 'age', 'coordinator', 'active']:
                continue
            setattr(cong_member, field.name, bool(request.POST.get(field.name, False)))

        cong_member.save()
        return redirect(request.path)


class CongregationMemberProfileRedirect(RedirectView):
    url = ""

    def get_redirect_url(self, *args, **kwargs):
        try:
            member = CongregationMember.objects.get(user=self.request.user)
            redirect_url = member.get_absolute_url()
        except exceptions.ObjectDoesNotExist:
            redirect_url = '/congregations/unknown/members/{member_id}'.format(member_id=self.request.user.id)

        return self.url + redirect_url