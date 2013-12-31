from base.tests.model_maker import clean_and_save
from cms.models import (
    Page,
    Section,
    Content,
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
    return Page.objects.get(name='home')


def get_section():
    return get_content_hatherleigh_two().section


def default_scenario_cms():
    default_moderate_state()
    page = clean_and_save(
        Page(
            name='home'
        )
    )
    section = clean_and_save(
        Section(
            page=page,
        )
    )
    clean_and_save(
        Content(
            section=section,
            order=1,
            moderate_state=ModerateState.pending(),
            title='Hatherleigh Three',
        )
    )
    clean_and_save(
        Content(
            section=section,
            order=1,
            moderate_state=ModerateState.published(),
            title='Hatherleigh Two',
        )
    )
    clean_and_save(
        Content(
            section=section,
            order=3,
            moderate_state=ModerateState.removed(),
            title='Hatherleigh Old',
        )
    )
    # Jacobstowe
    section2 = clean_and_save(
        Section(
            page=page,
        )
    )
    clean_and_save(
        Content(
            section=section2,
            order=2,
            moderate_state=ModerateState.published(),
            title='Jacobstowe One',
        )
    )
