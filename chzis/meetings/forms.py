from django.forms import ModelForm, TextInput, Select, Textarea, HiddenInput
from django import forms
from django.utils.translation import ugettext_lazy as _

from chzis.school.widgets import InlineSelectDateWidget
from chzis.meetings.models import MeetingTask, MeetingItem
from chzis.congregation.models import CongregationMemberPrivileges, CongregationMember


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None,
                 help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                               initial=initial, help_text=help_text, *args, **kwargs)


class MeetingTaskSchoolForm(forms.ModelForm):
    meeting_item = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select', 'label': None}))
    person = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select'}))

    def __init__(self, *args, **kwargs):
        master_school_members = (CongregationMember.school.master_or_reader(congregation=1)).values_list('member_id',
                                                                                                'member__user__last_name',
                                                                                                'member__user__first_name')
        master_school_members = [(member_id, u"{lastname} {firstname}".format(lastname=lastname, firstname=firstname))
                                 for member_id, lastname, firstname in master_school_members]

        super(MeetingTaskSchoolForm, self).__init__(*args, **kwargs)
        self.fields['meeting_item'].choices = [('', '-------------')] + list(
            MeetingItem.objects.filter(part__name="Field ministry").values_list('id', 'name'))
        self.fields['person'].choices = [('', '-------------')] + master_school_members

    class Meta:
        model = MeetingTask
        exclude = ['topic', 'description']

        widgets = {
            'topic': TextInput(attrs={'class': 'form-control'}),
            'presentation_date': InlineSelectDateWidget(attrs={'class': 'form-control chosen-select'},
                                                        empty_label=("Year", "Month", "Day")),
            'background': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
        }

    def clean_meeting_item(self):
        meetings_id = self.cleaned_data['meeting_item']
        meeting_item = MeetingItem.objects.get(id=meetings_id)
        return meeting_item

    def clean_person(self):
        member_id = self.cleaned_data['person']
        member = CongregationMember.objects.get(id=member_id)
        return member

    def as_div(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)


class MeetingTaskSchoolViewForm(forms.ModelForm):
    class Meta:
        model = MeetingTask
        exclude = ['topic', 'description']

        widgets = {
            'meeting_item': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'person': TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'presentation_date': InlineSelectDateWidget(attrs={'class': 'form-control', 'disabled': ''},
                                                        empty_label=("Year", "Month", "Day"),
                                                        ),
        }

    def as_div(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)
