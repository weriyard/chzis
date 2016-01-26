from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.core import exceptions

from chzis.users.models import PeopleProfile


class PeopleLogin(View):
    def get(self, request):
        return auth_views.login(request, template_name='login.html')

    def post(self, request):
        response = auth_views.login(request, template_name='login.html')
        if isinstance(response, HttpResponseRedirect):
            try:
                PeopleProfile.objects.get(user__username=request.POST.get('username'))
            except exceptions.ObjectDoesNotExist:
                people_profile = PeopleProfile()
                people_profile.user = request.user
                people_profile.save()
        return response


class PeopleProfileSetting(View):
    def get(self, request):
        pass

    def post(self, request):
        pass

