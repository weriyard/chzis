"""chzis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from chzis.mainpage.views import Index
from chzis.congregation.views import CongregationDetails, Congregations, CongregationMemberDetails
from chzis.users.views import PeopleProfileSetting, PeopleLogin
from chzis.school.views import Tasks, AddTasks, TaskView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^people/login$', auth_views.login, {'template_name': 'login.html'},
    #     name='login'),
    url(r'^people/login$', PeopleLogin.as_view(), name='login'),
    url(r'^people/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', Index.as_view()),
    url(r'^congregation/$', login_required(Congregations.as_view())),
    url(r'^congregation/(?P<congregation_id>\d+)/$', login_required(CongregationDetails.as_view())),
    url(r'^congregation/(?P<congregation_id>\d+)/members/(?P<member_id>\d+)$', CongregationMemberDetails.as_view()),
    url(r'^school/tasks/$', Tasks.as_view()),
    url(r'^school/tasks/add/$', AddTasks.as_view()),
    url(r'^school/tasks/(?P<task_id>\d+)/$', TaskView.as_view()),
    url(r'^people/profile/', PeopleProfileSetting.as_view()),


] + static(settings.STATIC_URL)

