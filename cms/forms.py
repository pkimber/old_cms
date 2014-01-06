from django import forms

from base.form_utils import RequiredFieldForm

from .models import (
    SimpleContent,
    TextContent,
)


class SimpleContentEmptyForm(forms.ModelForm):

    class Meta:
        model = SimpleContent
        fields = ()


class SimpleContentForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(SimpleContentForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = SimpleContent
        fields = (
            'title',
            'description',
            'picture',
        )


class TextContentEmptyForm(forms.ModelForm):

    class Meta:
        model = TextContent
        fields = ()


class TextContentForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(TextContentForm, self).__init__(*args, **kwargs)
        for name in ('title',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = TextContent
        fields = (
            'title',
        )
