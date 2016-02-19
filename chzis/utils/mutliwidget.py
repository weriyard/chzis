class ChooseLessonMultiWidget(MultiWidget):

    def __init__(self,  attrs=None, choices=()):
        self.choices = list(choices)
        widgets = [TextInput(attrs=attrs),
                   RadioSelect(choices=self.choices, attrs=attrs)]
        super(ChooseLessonMultiWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        print 'decompres', value
        if value:
            return [1,1]

        return [None, None]

    def aaa(self):
        return ":D:D:D:"

    def format_output(self, rendered_widgets):
        print 'f_out', rendered_widgets
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        print 'vvalue from datadict', data, files, name

    def render(self, name, value, attrs=None, choices=()):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            if isinstance(widget, RadioSelect):
                output.append(widget.render(name + '_%s' % i, widget_value, final_attrs, self.choices))
            else:
                output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))