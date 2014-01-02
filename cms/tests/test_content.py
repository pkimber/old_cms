from django.test import TestCase

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
    ModerateState,
)
from moderate.tests.scenario import default_moderate_state


class TestContent(TestCase):

    def setUp(self):
        default_moderate_state()
        self.page = make_page(name='home')
        self.section = make_section(self.page)
        make_content(
            self.section, 1, ModerateState.published(), 'Hatherleigh'
        )
        make_content(
            self.section, 3, ModerateState.pending(), 'Hatherleigh Pending'
        )

    def test_next_order(self):
        self.assertGreater(Content.objects.next_order(self.page), 3)
