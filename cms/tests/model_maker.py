from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from cms.models import (
    Container,
    Content,
    Layout,
    Page,
    Section,
)


def make_container(section, **kwargs):
    defaults = dict(
        section=section,
        **kwargs
    )
    defaults.update(kwargs)
    return clean_and_save(Container(**defaults))


def make_content(container, order, moderate_state, **kwargs):
    defaults = dict(
        container=container,
        order=order,
        moderate_state=moderate_state,
    )
    defaults.update(kwargs)
    return clean_and_save(Content(**defaults))


def make_layout(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(Layout(**defaults))


def make_page(name, order, **kwargs):
    defaults = dict(
        name=name,
        order=order,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(Page(**defaults))


def make_section(page, layout, **kwargs):
    defaults = dict(
        page=page,
        layout=layout,
        **kwargs
    )
    defaults.update(kwargs)
    return clean_and_save(Section(**defaults))
