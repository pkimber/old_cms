from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    #Content,
    Page,
    Section,
)
from cms.tests.model_maker import (
    make_container,
    #make_content,
    make_layout,
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
        page = make_page('home', 0)
        body = make_layout('body')
        self.section = make_section(page, body)
        container = make_container(self.section, 1)
        #make_content(container, 1, ModerateState.published())
        #make_content(container, 3, ModerateState.pending())

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass
