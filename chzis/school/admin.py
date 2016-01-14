from django.contrib import admin
from chzis.school.models import Lesson, Background, SchoolTask

class LessonAdmin(admin.ModelAdmin):
    pass


class BackgroundAdmin(admin.ModelAdmin):
    pass


class SchoolTaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Background, LessonAdmin)
admin.site.register(SchoolTask, SchoolTaskAdmin)