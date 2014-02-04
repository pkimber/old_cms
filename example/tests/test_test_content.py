from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    ModerateState,
    Page,
    Section,
)
from cms.tests.model_maker import (
    make_container,
    make_layout,
    make_page,
    make_section,
)
from cms.tests.scenario import default_moderate_state
from example.models import TestContent
from example.tests.model_maker import make_test_content


class TestTestContent(TestCase):

    def setUp(self):
        default_moderate_state()
        page = make_page('home', 0)
        body = make_layout('body')
        self.section = make_section(page, body)

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass

    def test_pending_order(self):
        """Pending items should by in 'order' order."""
        make_test_content(
            make_container(self.section, 5),
            ModerateState.pending(),
            'XYZ'
        )
        make_test_content(
            make_container(self.section, 3),
            ModerateState.published(),
            'LMN'
        )
        make_test_content(
            make_container(self.section, 1),
            ModerateState.pending(),
            'ABC'
        )
        pending = TestContent.objects.pending(self.section)
        self.assertListEqual(
            ['XYZ', 'LMN', 'ABC'],
            [t.title for t in pending]
        )

    def test_published_order(self):
        """Published items should by in 'order' order."""
        make_test_content(
            make_container(self.section, 9),
            ModerateState.published(),
            'XYZ'
        )
        make_test_content(
            make_container(self.section, 8),
            ModerateState.published(),
            'ABC'
        )
        published = TestContent.objects.published(self.section)
        self.assertListEqual(
            ['XYZ', 'ABC'],
            [t.title for t in published]
        )
