from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    Page,
    Section,
    Content,
)
from moderate.models import (
    ModerateState,
)
from moderate.tests.scenario import default_moderate_state


class TestContent(TestCase):

    def setUp(self):
        default_moderate_state()
        self.page = clean_and_save(
            Page(
                name='home'
            )
        )
        self.section = clean_and_save(
            Section(
                page=self.page,
            )
        )
        clean_and_save(
            Content(
                section=self.section,
                order=1,
                moderate_state=ModerateState.published(),
                title='Hatherleigh',
            )
        )
        clean_and_save(
            Content(
                section=self.section,
                order=3,
                moderate_state=ModerateState.pending(),
                title='Hatherleigh Pending',
            )
        )

    def test_next_order(self):
        self.assertGreater(Content.objects.next_order(self.page), 3)
