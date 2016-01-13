from django.contrib import admin
from chzis.meetings.models import MeetingType, MeetingPart, MeetingItem


class MeetingTypeAdmin(admin.ModelAdmin):
    pass


class MeetingPartAdmin(admin.ModelAdmin):
    pass


class MeetingItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(MeetingType, MeetingTypeAdmin)
admin.site.register(MeetingPart, MeetingPartAdmin)
admin.site.register(MeetingItem, MeetingItemAdmin)
