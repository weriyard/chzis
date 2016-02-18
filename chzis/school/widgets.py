from django.forms import SelectDateWidget, Widget, RadioSelect, TextInput, ChoiceField, CheckboxInput, MultiWidget, MultiValueField, CharField
from django.forms import widgets
from django.utils.safestring import mark_safe
import copy

from chzis.school.models import Lesson


class InlineSelectDateWidget(SelectDateWidget):
    def render(self, name, value, attrs=None):
        render_output = super(InlineSelectDateWidget, self).render(name, value, attrs=None)
        output = '<div class="form-inline">%s</div>'
        return output % render_output


class LessonPassedWidget(Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            css_class = "label-default"
            label = "None"
        elif value:
            css_class = "label-success"
            label = "PASSED"
        else:
            css_class = "label-danger"
            label = "FAIL"
        html = '<h3 class="lesson-passed">' \
               '<span class="label %s">%s</span>' \
               '</h3>' % (css_class, label)
        return mark_safe("%s" % html)


class LessonListWithLastDate(Widget):
    def __init__(self, *args, **kwargs):
        super(LessonListWithLastDate, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        return "llaaldsffdsf"

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        return data.get(name)

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        memo[id(self)] = obj
        return obj


class AwesomeCheckbox(CheckboxInput):
    def render(self, name, value, attrs=None):
        render = super(AwesomeCheckbox, self).render(name, value, attrs)
        return "<div class='%s'>%s<label for='%s'></label></div>" % (self.attrs.get('class'), render, attrs.get('id'))


class ChooseLessonMultiWidget(MultiWidget):

    def __init__(self, *args, **kwargs):
        _widgets = (RadioSelect(), TextInput)
        super(ChooseLessonMultiWidget, self).__init__(_widgets, attrs={})

    def decompress(self, value):
        print 'decompres', value
        if value:
            return [1,1]

        return [None, None]

    # def format_output(self, rendered_widgets):
    #     print 'f_out', rendered_widgets
    #     return u''.join(rendered_widgets)
    #
    # def value_from_datadict(self, data, files, name):
    #     print 'vvalue from datadict', data, files, name
    def to_python(self, value):
        print value


class ChooseLessonMultiField(MultiValueField):

    def __init__(self, *args, **kwargs):
        print args, kwargs
        widget = ChooseLessonMultiWidget
        print 'gownooooooooooooo'
        _fields = (ChoiceField(), CharField())
        super(ChooseLessonMultiField, self).__init__(fields=_fields, widget=widget, *args, **kwargs)

    def compress(self, data_list):
        print data_list
        return

    def to_python(self, value):
        print value

    def clean(self, value):
        print value