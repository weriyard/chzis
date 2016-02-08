from django.contrib import admin
from chzis.meetings.models import MeetingType, MeetingPart, MeetingItem, MeetingTask


class MeetingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time')
    list_filter = ('name', 'start_time')


class MeetingPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_name')
    list_filter = ('name', 'type')

    def type_name(self, obj):
        return obj.type.name


class MeetingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'part')
    list_filter = list_display


class MeetingTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting_item', 'person', 'presentation_date')
    list_filter = list_display


admin.site.register(MeetingType, MeetingTypeAdmin)
admin.site.register(MeetingPart, MeetingPartAdmin)
admin.site.register(MeetingItem, MeetingItemAdmin)
admin.site.register(MeetingTask, MeetingTaskAdmin)