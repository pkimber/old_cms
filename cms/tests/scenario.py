from base.tests.model_maker import clean_and_save
from cms.models import (
    Page,
    Section,
    Content,
)
from cms.tests.model_maker import (
    make_content,
    make_page,
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


def get_page_home():
    return Page.objects.get(slug='home')


def get_page_information():
    return Page.objects.get(slug='information')


def get_section():
    return get_content_hatherleigh_two().section


def default_scenario_cms():
    default_moderate_state()
    page = make_page('Home', 0)
    section = make_section(page=page)
    make_content(section, 1, ModerateState.pending(), 'Hatherleigh Three')
    make_content(section, 1, ModerateState.published(), 'Hatherleigh Two')
    make_content(section, 3, ModerateState.removed(), 'Hatherleigh Old')
    # Jacobstowe
    section2 = make_section(page=page)
    make_content(section2, 2, ModerateState.published(), 'Jacobstowe One')
    # Information page
    page_info = make_page('Information', 1)
    section_info = make_section(page_info)
    make_content(section_info, 1, ModerateState.published(), 'Monkokehampton')
