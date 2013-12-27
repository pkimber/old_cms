from django import forms

from base.form_utils import (
    RequiredFieldForm,
)
from .models import (
    Section,
)


class SectionEmptyForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ()


class SectionForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Section
        fields = (
            'title',
            'description',
            'picture',
        )
