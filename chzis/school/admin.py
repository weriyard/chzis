from django.contrib import admin
from chzis.school.models import Lesson, Background, StudentProfile

class LessonAdmin(admin.ModelAdmin):
    pass


class BackgroundAdmin(admin.ModelAdmin):
    pass


class StudentProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Background, LessonAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
