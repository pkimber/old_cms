from base.tests.model_maker import clean_and_save
from cms.models import (
    Layout,
    Page,
    Section,
    Content,
)
from cms.tests.model_maker import (
    make_container,
    make_content,
    make_page,
    make_layout,
    make_section,
)
from moderate.models import (
    ModerateError,
    ModerateState,
)
from moderate.tests.scenario import default_moderate_state


def get_content_hatherleigh_old():
    return Content.objects.get(title='Hatherleigh Old')


def get_content_hatherleigh_two():
    return Content.objects.get(title='Hatherleigh Two')


def get_content_hatherleigh_three():
    return Content.objects.get(title='Hatherleigh Three')


def get_content_jacobstowe_one():
    return Content.objects.get(title='Jacobstowe One')


def get_layout_body():
    return Layout.objects.get(slug='body')


def get_page_home():
    return Page.objects.get(slug='home')


def get_page_information():
    return Page.objects.get(slug='information')


def get_container_hatherleigh_two():
    return get_content_hatherleigh_two().container


def default_scenario_cms():
    default_moderate_state()
    page = make_page('Home', 0)
    body = make_layout('Body')
    footer = make_layout('Footer')
    section = make_section(page, body)
    # Home, Hatherleigh
    container_hatherleigh = make_container(section)
    make_content(
        container_hatherleigh, 1, ModerateState.pending(), 'Hatherleigh Three'
    )
    make_content(
        container_hatherleigh, 1, ModerateState.published(), 'Hatherleigh Two'
    )
    make_content(
        container_hatherleigh, 3, ModerateState.removed(), 'Hatherleigh Old'
    )
    # Home, Jacobstowe
    container_jacobstowe = make_container(section)
    make_content(
        container_jacobstowe, 2, ModerateState.published(), 'Jacobstowe One'
    )
    # Home, Footer
    home_footer = make_section(page, footer)
    container_footer = make_container(home_footer)
    make_content(
        container_footer, 1, ModerateState.published(), 'Villages for You'
    )
    # Information, Monkokehampton
    page_info = make_page('Information', 1)
    section_info = make_section(page_info, body)
    container_monkokehampton = make_container(section_info)
    make_content(
        container_monkokehampton,
        1,
        ModerateState.published(),
        'Monkokehampton'
    )
