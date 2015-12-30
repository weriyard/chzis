from django.contrib import admin
from chzis.congregation.models import Congregation, CongregationMember

class CongregationAdmin(admin.ModelAdmin):
    pass


class CongregationMemberAdmin(admin.ModelAdmin):
    pass


admin.site.register(Congregation, CongregationAdmin)
admin.site.register(CongregationMember, CongregationMemberAdmin)
