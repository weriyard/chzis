from django.forms import ModelForm, TextInput, Select, Textarea, RadioSelect, ChoiceField
from django import forms
from chzis.school.models import SchoolTask, Lesson, Background
from chzis.school.widgets import InlineSelectDateWidget, LessonPassedWidget, LessonListWithLastDate
from chzis.congregation.models import CongregationMember
from chzis.meetings.models import MeetingItem, MeetingTask


class SchoolTaskForm(ModelForm):

    class Meta:
        model = SchoolTask
        exclude = ['task', 'lesson_passed']
        widgets = {
            'lesson': RadioSelect(attrs={'class': 'radio-primary'}),
            #'lesson': LessonListWithLastDate(attrs={'class': 'form-control'}),
            'background': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})

        }

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th></tr><tr><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)

    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row='<div class="form-group %(html_class_attr)s">%(errors)s %(label)s %(field)s %(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <div class="help-block">%s</div>',
            errors_on_separate_row=True)


class SchoolTaskViewForm(SchoolTaskForm):
    class Meta:
        model = SchoolTask
        exclude = ['task']
        widgets = {
            'lesson': TextInput(attrs={'class': 'form-control', 'disabled':''}),
            'lesson_passed': LessonPassedWidget(attrs={'class': 'form-control', 'disabled':''}),
            'background': TextInput(attrs={'class': 'form-control', 'disabled':''}),
            'description': Textarea(attrs={'class': 'form-control', 'disabled':''})
        }


class SchoolTaskForm2(ModelForm):
    meeting_item = forms.ModelChoiceField(queryset=MeetingTask.objects.filter(meeting_item__part__name=""))
    person = forms.ModelChoiceField(queryset=CongregationMember.objects.filter(school_allow=True))
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all())
    backgrounds = forms.ModelChoiceField(queryset=Background.objects.all())
    presentation_date = forms.SelectDateWidget()
    description = forms.Textarea()



