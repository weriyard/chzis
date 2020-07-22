from collections import OrderedDict

from django.forms import TextInput, Select, Textarea, DateField
from django import forms
from django.utils.translation import gettext as _

from chzis.school.widgets import InlineSelectDateWidget
from chzis.meetings.models import MeetingTask, MeetingItem
from chzis.congregation.models import CongregationMemberPrivileges, CongregationMember


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None,
                 help_text=None, *args, **kwargs):

        if empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label,
                                               initial=initial, help_text=help_text, *args, **kwargs)


class MeetingTaskSchoolForm(forms.ModelForm):
    meeting_item = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select'}),
                                    label=_("Meeting item"),
                                    label_suffix="")
    person = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select'}),
                              label=_("Main"),
                              label_suffix="")
    presentation_date = DateField(widget=InlineSelectDateWidget(attrs={'class': 'form-control chosen-select'},
                                                                empty_label=("Year", "Month", "Day")),
                                  label=_("Presentation date"), label_suffix="")

    def __init__(self, *args, **kwargs):
        congregation = kwargs.pop('congregation')
        kwargs.setdefault('label_suffix', '')
        main_school_members = (CongregationMember.school.main_or_reader(congregation=congregation)).values_list(
            'member_id',
            'member__user__last_name',
            'member__user__first_name')
        main_school_members = [(member_id, u"{lastname} {firstname}".format(lastname=lastname, firstname=firstname))
                                 for member_id, lastname, firstname in main_school_members]

        super(MeetingTaskSchoolForm, self).__init__(*args, **kwargs)
        bible_reading = MeetingItem.objects.filter(name="Bible Reading").values_list('id', 'full_name')
        field_ministy_items = MeetingItem.objects.filter(part__name="Field ministry").values_list('id', 'full_name').exclude(name='Month presentations')
        school_meeting_items = list()
        school_meeting_items.append(('', '-------------'))
        school_meeting_items.extend(bible_reading)
        school_meeting_items.extend(field_ministy_items)
        self.fields['meeting_item'].choices = school_meeting_items
        self.fields['person'].choices = [('', '-------------')] + main_school_members
        self.move_field_after('person', 'presentation_date')

    def move_field_after(self, field, after_field=None):
        mv_field = self.fields.pop(field)
        new_fields_order = OrderedDict()

        if after_field is None:
            new_fields_order[field] = mv_field

        for field_name, field_obj in self.fields.items():
            new_fields_order[field_name] = field_obj
            if after_field == field_name:
                new_fields_order[field] = mv_field

        self.fields = new_fields_order

    class Meta:
        model = MeetingTask
        exclude = ['topic', 'description']

        widgets = {
            'topic': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
        }

        labels = {
            'topic': _("Topic"),
            'description': _("Description")
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

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MeetingTaskSchoolViewForm, self).__init__(*args, **kwargs)
        self.move_field_after('person', 'presentation_date')

    def move_field_after(self, field, after_field=None):
        mv_field = self.fields.pop(field)
        new_fields_order = OrderedDict()

        if after_field is None:
            new_fields_order[field] = mv_field

        for field_name, field_obj in self.fields.items():
            new_fields_order[field_name] = field_obj
            if after_field == field_name:
                new_fields_order[field] = mv_field

        self.fields = new_fields_order


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

        labels = {
            'person': _("Main"),
            'meeting_item': _("Meeting item"),
            'presentation_date': _("Presentation date")
        }

    def as_div(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
                normal_row='<div class="form-group %(html_class_attr)s">%(label)s %(field)s%(help_text)s</div>',
                error_row='<div class="error-block">%s</div>',
                row_ender='</div>',
                help_text_html=' <div class="help-block">%s</div>',
                errors_on_separate_row=True)
