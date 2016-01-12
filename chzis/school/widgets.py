from django.forms import SelectDateWidget
from django.utils.safestring import mark_safe


class InlineSelectDateWidget(SelectDateWidget):

    def render(self, name, value, attrs=None):
        render_output = super(InlineSelectDateWidget, self).render(name, value, attrs=None)
        output = '<div class="form-inline">%s</div>'
        return output % render_output