from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from cms.models import (
    ModerateState,
    Section,
    Simple,
)


def make_moderate_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(ModerateState(**defaults))


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
