from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.conf import settings

class Index(View):

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return render(request, 'index.html', {})

