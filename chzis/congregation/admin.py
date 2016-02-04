from django.contrib import admin
from chzis.congregation.models import Congregation, CongregationMember, CongregationPrivileges, CongregationMemberPrivileges

class CongregationAdmin(admin.ModelAdmin):
    pass


class CongregationMemberAdmin(admin.ModelAdmin):
    pass


class CongregationPrivilegesAdmin(admin.ModelAdmin):
    pass


class CongregationMemberPrivilegesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Congregation, CongregationAdmin)
admin.site.register(CongregationMember, CongregationMemberAdmin)
admin.site.register(CongregationPrivileges, CongregationPrivilegesAdmin)
admin.site.register(CongregationMemberPrivileges, CongregationMemberPrivilegesAdmin)
