from base.tests.model_maker import clean_and_save

from cms.models import (
    Section,
    Simple,
)


def make_section(name, **kwargs):
    return clean_and_save(
        Section(
            name=name,
            **kwargs
        )
    )


def make_simple(section, order, title, **kwargs):
    return clean_and_save(
        Simple(
            section=section,
            order=order,
            title=title,
            **kwargs
        )
    )
