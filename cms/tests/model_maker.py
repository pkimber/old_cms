from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from cms.models import (
    ModerateState,
    Page,
    Section,
)


def make_moderate_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(ModerateState(**defaults))


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
