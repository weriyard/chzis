from django.shortcuts import render
from django.views.generic import View, TemplateView, RedirectView
from django.shortcuts import redirect
from django.core import exceptions
from django.db.models import Q

from chzis.congregation.models import Congregation, CongregationMember, CongregationMemberPrivileges, \
    CongregationPrivileges


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
        priv_cong_members = CongregationMemberPrivileges.objects.filter(member__congregation_id=congregation_id)

        members = {}
        for cong_member in cong_members:
            member_privileges = members.setdefault(cong_member.id, {})
            member_privileges['member'] = cong_member
            priv_cong_member = priv_cong_members.filter(member=cong_member)
            privileges = member_privileges.setdefault('privileges', {'active': cong_member.active})
            for priv in priv_cong_member:
                privileges[priv.privilege.name] = True

        context = dict()
        context['cong_members'] = members
        return context


class CongregationMemberDetails(TemplateView):
    template_name = "congregationMember.html"

    def get_context_data(self, member_id, *args, **kwargs):
        context = dict()

        if 'congregation_id' in kwargs:
            cong_member = CongregationMember.objects.get(congregation__id=kwargs.get('congregation_id'),
                                                         user__id=member_id)
        else:
            try:
                cong_member = CongregationMember.objects.get(user__id=member_id)
            except exceptions.ObjectDoesNotExist as e:
                return context

        member_privileges = CongregationMemberPrivileges.objects.filter(member=cong_member).values_list(
            'privilege__name', 'id')
        all_allowed_privileges = CongregationPrivileges.objects.filter(
            Q(allow_gender=cong_member.user.profile.gender) | Q(allow_gender='A')).values('id', 'name', 'full_name')
        current_member_privileges = dict(member_privileges)

        if cong_member is not None:
            member_privileges = []
            for priv in all_allowed_privileges:
                priv_id = current_member_privileges.get(priv['name'], None)
                pr = dict(name=priv['name'], id=priv_id, full_name=priv['full_name'])
                member_privileges.append(pr)

            context['member_privileges'] = member_privileges

        context['member'] = cong_member
        return context

    def post(self, request, congregation_id, member_id):
        cong_member = CongregationMember.objects.get(id=member_id)
        all_allowed_privileges = CongregationPrivileges.objects.filter(
                Q(allow_gender=cong_member.user.profile.gender) | Q(allow_gender='A')).values('id', 'name', 'full_name')
        current_privs = CongregationMemberPrivileges.objects.filter(member=cong_member).values_list('id', 'privilege__name')
        set_last_modification = False

        for priv in all_allowed_privileges:
            if priv['name'] in request.POST and request.POST[priv['name']] == 'None':
                cmp = CongregationMemberPrivileges()
                cmp.member = cong_member
                cmp.privilege = CongregationPrivileges.objects.get(name=priv['name'])
                cmp.save()
                set_last_modification = True

        for priv_id, priv_name in current_privs:
            if priv_name not in request.POST:
                CongregationMemberPrivileges.objects.get(id=priv_id).delete()
                cong_member.save(force_update=True)
                set_last_modification = True

        if set_last_modification:
            cong_member.save(force_update=True)

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
