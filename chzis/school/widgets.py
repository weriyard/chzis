from django.forms import SelectDateWidget, Widget
from django.utils.safestring import mark_safe


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

