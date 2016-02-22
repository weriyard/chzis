from django.forms import ModelForm, TextInput, Select, Textarea, HiddenInput
from django import forms
from django.utils.translation import ugettext_lazy as _

from chzis.school.widgets import InlineSelectDateWidget
from chzis.meetings.models import MeetingTask, MeetingItem


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)


class MeetingTaskSchoolForm(forms.ModelForm):
    meeting_item = EmptyChoiceField(widget=Select(attrs={'class': 'form-control chosen-select', 'label': None}), empty_label='---------')

    def __init__(self, *args, **kwargs):
        super(MeetingTaskSchoolForm, self).__init__(*args, **kwargs)
        meeting_item_choices = MeetingItem.objects.filter(part__name="Field ministry").values_list('id', 'name')
        self.fields['meeting_item'].choices = meeting_item_choices

    class Meta:
        model = MeetingTask
        exclude = ['topic', 'description']

        widgets = {
            'person': Select(attrs={'class': 'form-control chosen-select fix-select-style'}),
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
