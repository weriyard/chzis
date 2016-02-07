from django.forms import ModelForm, TextInput, Select, Textarea, RadioSelect, ChoiceField
from django import forms
from django.utils.translation import ugettext as _

from chzis.school.models import SchoolTask, Lesson, Background
from chzis.school.widgets import InlineSelectDateWidget, LessonPassedWidget, AwesomeCheckbox


class SchoolTaskForm(ModelForm):
    class Meta:
        model = SchoolTask
        exclude = ['task', 'lesson_passed', 'supervisor']
        widgets = {
            'slave': Select(attrs={'class': 'form-control'}),
            'lesson': RadioSelect(attrs={'class': 'radio-primary'}),
            # 'lesson': LessonListWithLastDate(attrs={'class': 'form-control'}),
            'background': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})

        }

    def as_table(self):
        return self._html_output(
                normal_row='<tr%(html_class_attr)s><th>%(label)s</th></tr><tr><td>%(errors)s%(field)s%(help_text)s</td></tr>',
                error_row='<tr><td colspan="2">%s</td></tr>',
                row_ender='</td></tr>',
                help_text_html='<br /><span class="helptext">%s</span>',
                errors_on_separate_row=False)

    def as_div(self):
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
            'slave': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'supervisor': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'lesson': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'lesson_passed': LessonPassedWidget(attrs={'class': 'form-control', 'disabled': ''}),
            'background': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'description': Textarea(attrs={'class': 'form-control', 'disabled': ''})
        }


class SchoolTaskFilterForm(forms.Form):
    start_active = forms.BooleanField(
        widget=AwesomeCheckbox(attrs={"class": "checkbox checkbox-default checkbox-filter-date"}),
        label="",
        initial=False, required=False)
    start = forms.DateField(widget=InlineSelectDateWidget(attrs={'class': 'form-control'},
                                                          empty_label=(_("Year"), _("Month"), _("Day"))),
                            label="", required=False)
    end_active = forms.BooleanField(
        widget=AwesomeCheckbox(attrs={"class": "checkbox checkbox-default checkbox-filter-date"}),
        label="",
        initial=False, required=False)
    end = forms.DateField(widget=InlineSelectDateWidget(attrs={'class': 'form-control'},
                                                        empty_label=(_("Year"), _("Month"), _("Day"))),
                          label="", required=False)

    def clean_end(self):
        data = self.cleaned_data['end']
        return data

    def as_div(self):
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)
