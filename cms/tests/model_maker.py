from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from cms.models import (
    Content,
    Page,
    Section,
)


def make_content(section, order, moderate_state, title, **kwargs):
    defaults = dict(
        section=section,
        order=order,
        moderate_state=moderate_state,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(Content(**defaults))


def make_page(name, order, **kwargs):
    defaults = dict(
        name=name,
        order=order,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(Page(**defaults))


def make_section(page, **kwargs):
    defaults = dict(
        page=page,
        **kwargs
    )
    defaults.update(kwargs)
    return clean_and_save(Section(**defaults))
