from django.contrib import admin
from chzis.users.models import People


class PeopleAdmin(admin.ModelAdmin):
    pass


admin.site.register(People, PeopleAdmin)
