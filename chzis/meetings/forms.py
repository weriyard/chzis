from django.forms import ModelForm, TextInput, Select, Textarea
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
    meeting_item_choices = MeetingItem.objects.filter(part__name="Field ministry").values_list('id', 'name')
    meeting_item = EmptyChoiceField(choices=[(id, _(item)) for id, item in meeting_item_choices],
                                     widget=Select(attrs={'class': 'form-control', 'label': None}), empty_label='---------')

    class Meta:
        model = MeetingTask
        exclude = ['topic', 'description']

        widgets = {
            'person': Select(attrs={'class': 'form-control'}),
            'topic': TextInput(attrs={'class': 'form-control'}),
            'presentation_date': InlineSelectDateWidget(attrs={'class': 'form-control'},
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
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <div class="help-block">%s</div>',
            errors_on_separate_row=True)
