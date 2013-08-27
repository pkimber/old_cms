from base.tests.model_maker import clean_and_save

from cms.models import Section


def make_section(name, **kwargs):
    return clean_and_save(
        Section(
            name=name,
            **kwargs
        )
    )
