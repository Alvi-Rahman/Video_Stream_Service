from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django import forms


class PictureWidget(forms.widgets.Widget):
    def __init__(self, *args, **kwargs):
        self._id = kwargs.pop('id', None)
        self.link = kwargs.pop('link', None)
        self.video = kwargs.pop('video', False)
        super(PictureWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if self.video:
            html = Template("""<video width="320" height="240" controls>
                                   <source src="$link" id="$id" type="video/mp4">
                                </video>""")
        else:
            html = Template("""<img src="$link" id="$id" width="320px"/>""")
        return mark_safe(html.substitute(link=self.link, id=self._id))
