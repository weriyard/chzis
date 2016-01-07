from django.forms import ModelForm, SelectDateWidget
from django.contrib.admin import widgets
from chzis.school.models import SchoolTask


class SchoolTaskForm(ModelForm):
    class Meta:
        model = SchoolTask
        fields = '__all__'
        widgets = {
            #'presentation_date': widgets.AdminDateWidget(),
            'presentation_date': SelectDateWidget()
        }

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th></tr><tr><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)