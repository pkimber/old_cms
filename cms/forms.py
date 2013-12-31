from django import forms

from base.form_utils import (
    RequiredFieldForm,
)
from .models import (
    Content,
)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ()


class ContentForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Content
        fields = (
            'title',
            'description',
            'picture',
        )
