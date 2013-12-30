from base.tests.model_maker import clean_and_save

from cms.models import (
    Page,
    Section,
)


def make_page(name, **kwargs):
    return clean_and_save(
        Page(
            name=name,
            **kwargs
        )
    )


def make_section(section, order, title, **kwargs):
    return clean_and_save(
        Section(
            section=section,
            order=order,
            title=title,
            **kwargs
        )
    )
