from django.contrib import admin
from chzis.users.models import PeopleProfile


class PeopleProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(PeopleProfile, PeopleProfileAdmin)
