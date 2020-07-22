import datetime

from django.forms import ModelForm, TextInput, Select, Textarea, RadioSelect, HiddenInput, ValidationError
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as __
from django.core import exceptions
from chzis.school.models import SchoolTask, Lesson
from chzis.school.widgets import InlineSelectDateWidget, LessonPassedWidget, AwesomeCheckbox
from chzis.congregation.models import CongregationMember
from chzis.meetings.forms import EmptyChoiceField


class SchoolTaskForm(ModelForm):
    lesson_number = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select'}),
                                     label=_("Lesson number"),
                                     required=False)
    subordinate = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select'}),
                             label=_("Subordinate"),
                             required=False)

    def __init__(self, *args, **kwargs):
        congregation = kwargs.pop('congregation')
        kwargs.setdefault('label_suffix', '')
        subordinate_school_members = (CongregationMember.school.subordinate(congregation=congregation)).values_list('member_id',
                                                                                                        'member__user__last_name',
                                                                                                        'member__user__first_name')
        subordinate_school_members = [(member_id, u"{lastname} {firstname}".format(lastname=lastname, firstname=firstname))
                                for member_id, lastname, firstname in subordinate_school_members]
        lessons_list = Lesson.objects.all().values_list('id', 'number', 'name')
        lessons_list = [(lesson_id, u"{number} {name}".format(number=number, name=name)) for lesson_id, number, name in
                        lessons_list]
        super(SchoolTaskForm, self).__init__(*args, **kwargs)
        self.fields['lesson'].required = False
        self.fields['subordinate'].choices = [('', '-------------')] + subordinate_school_members
        self.fields['lesson_number'].choices = [('', '-------------')] + lessons_list

    class Meta:
        model = SchoolTask
        exclude = ['task', 'lesson_passed', 'supervisor', 'lesson_passed_date', 'background']
        widgets = {
            'id': HiddenInput(),
            'lesson': RadioSelect(attrs={'class': 'radio-primary'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

        labels = {
            'lesson': _("Lesson"),
            'description': _("Description")
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

    def clean_subordinate(self):
        main_member_id = self.data.get('person')
        if len(main_member_id) > 0:
            main_member = CongregationMember.objects.get(id=main_member_id)

        member_id = self.cleaned_data.get('subordinate')
        if len(member_id) > 0:
            member = CongregationMember.objects.get(id=member_id)
            if member.id == main_member.id:
                raise ValidationError(_("Main and subordinate person must be unique in one task !"))
        else:
            member = None
        return member

    def clean_lesson_number(self):
        number_lesson_data = self.data.get('lesson_number')
        if number_lesson_data is not None and len(number_lesson_data.strip()) == 0:
            number_lesson_data = None
        lesson_data = self.data.get('lesson')

        if number_lesson_data is None and lesson_data is None:
            raise ValidationError(_("Lesson is required. Put lesson number or select from list (clean_lesson_number)."))
        elif number_lesson_data is not None and lesson_data is None:
            self.cleaned_data['lesson'] = Lesson.objects.get(number=number_lesson_data)
        elif number_lesson_data is not None and lesson_data is not None:
            raise ValidationError(_("Only one lesson number is allowed (clean_lesson_number) !"))

        return self.cleaned_data.get('lesson')

    def clean_lesson(self):
        number_lesson_data = self.data.get('lesson_number')
        if number_lesson_data is not None and len(number_lesson_data.strip()) == 0:
            number_lesson_data = None

        lesson_data = self.cleaned_data.get('lesson')
        if number_lesson_data is None and lesson_data is None:
            raise ValidationError(_("Lesson is required. Put lesson number or select from list (clean_lesson)."))
        elif lesson_data is None and number_lesson_data is not None:
            lesson_data = Lesson.objects.get(number=number_lesson_data)
        elif number_lesson_data is not None and lesson_data is not None:
            raise ValidationError(_("Only one lesson number is allowed (clean_lesson) !"))

        return lesson_data


class SchoolTaskViewForm(SchoolTaskForm):
    subordinate = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'disabled': ''}), label=_("Subordinate"),
                            label_suffix="", required=False)
    lesson_number = forms.CharField(widget=HiddenInput(), label=_("Lesson number"), label_suffix="")

    class Meta:
        model = SchoolTask
        exclude = ['task', 'lesson_passed_date', 'lesson_number', 'background']
        widgets = {
            'supervisor': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'lesson_passed': LessonPassedWidget(attrs={'class': 'form-control', 'disabled': ''}),
            'description': Textarea(attrs={'class': 'form-control', 'disabled': ''}),
            'creator': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'lesson': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
        }

        labels = {
            'lesson': _("Lesson"),
            'lesson_passed': _("Lesson passed"),
            'description': _("Description"),
            'creator': _("Creator"),
            'supervisor': _("Supervisor")
        }


class SchoolTaskFilterForm(forms.Form):

    start_active = forms.BooleanField(
            widget=AwesomeCheckbox(attrs={"class": "checkbox checkbox-default checkbox-filter-date"}),
            label="",
            initial=False, required=False)
    current_year = datetime.datetime.now().year
    year_range = range(current_year - 2, current_year + 6)
    start = forms.DateField(widget=InlineSelectDateWidget(attrs={'class': 'form-control'},
                                                          years=year_range,
                                                          empty_label=(_("Year"), _("Month"), _("Day"))),
                            label="", required=False)
    end_active = forms.BooleanField(
            widget=AwesomeCheckbox(attrs={"class": "checkbox checkbox-default checkbox-filter-date"}),
            label="",
            initial=False, required=False)
    end = forms.DateField(widget=InlineSelectDateWidget(attrs={'class': 'form-control'},
                                                        years=year_range,
                                                        empty_label=(_("Year"), _("Month"), _("Day"))),
                          label="", required=False)

    def as_div(self):
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)


class PassedLessonImportForm(forms.Form):
    passed_lessons = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                     label=_("Passed lessons"),
                                     label_suffix="")
    members = forms.CharField(widget=Select(attrs={'class': 'form-control'}),
                              label=_("School member"),
                              label_suffix="")

    def __init__(self, *args, **kwargs):
        super(PassedLessonImportForm, self).__init__(*args, **kwargs)
        congr_members_choices = CongregationMember.objects.filter(congregation_id=1).values_list('id',
                                                                                                 'user__last_name',
                                                                                                 'user__first_name')
        self.fields['members'].widget.choices = [(id, u"{0} {1}".format(last, first)) for id, last, first in
                                                 congr_members_choices]

    def as_div(self):
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)

    def clean_passed_lessons(self):
        data = self.cleaned_data['passed_lessons']
        data = data.strip()

        if ',' in data:
            split_data = data.split(",")
        elif ';' in data:
            split_data = data.split(';')
        else:
            split_data = [data]

        split_data = [val for val in split_data if len(val.strip()) > 0]

        for val in split_data:
            try:
                Lesson.objects.get(number=int(val))
            except ValueError:
                raise ValidationError(__("Only decimal numbers are allowed! Value '%(val)s' is wrong." % dict(val=val)))
            except exceptions.ObjectDoesNotExist:
                raise ValidationError(__("Lesson %(val)s doesn't exists!" % dict(val=val)))

        return split_data
