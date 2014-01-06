from django.db import IntegrityError
from django.db import models
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    Content,
    SimpleContent,
)
from cms.tests.scenario import (
    default_scenario_cms,
    get_container_hatherleigh_two,
    get_hatherleigh_old,
    get_hatherleigh_three,
    get_hatherleigh_two,
    get_jacobstowe_one,
    get_monkokehampton,
    get_layout_body,
    get_page_home,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)
from moderate.models import (
    ModerateError,
    ModerateState,
)
from moderate.tests.scenario import default_moderate_state


class TestModerate(TestCase):

    def setUp(self):
        default_moderate_state()
        default_scenario_login()
        default_scenario_cms()

    def test_is_pending(self):
        self.assertTrue(get_hatherleigh_three().content.is_pending)

    def test_is_published(self):
        self.assertTrue(get_hatherleigh_two().content.is_published)

    def test_is_removed(self):
        self.assertTrue(get_hatherleigh_old().content.is_removed)

    def test_two_pending_error(self):
        container = get_container_hatherleigh_two()
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            Content(
                container=container,
                moderate_state=ModerateState.pending(),
            )
        )

    def test_published(self):
        page = get_page_home()
        layout = get_layout_body()
        result = [
            c.title for c in SimpleContent.objects.published(page, layout)
        ]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_pending(self):
        page = get_page_home()
        layout = get_layout_body()
        result = [c.title for c in SimpleContent.objects.pending(page, layout)]
        self.assertListEqual(
            ['Hatherleigh Three', 'Jacobstowe One'],
            result
        )

    def test_publish_not_pending(self):
        """This content is not 'pending' so cannot be published."""
        c = get_hatherleigh_two()
        self.assertRaises(
            ModerateError,
            c.content.set_published,
            get_user_staff(),
        )

    def test_publish(self):
        c = get_hatherleigh_three()
        c.content.set_published(get_user_staff())
        c.content.save()
        page = get_page_home()
        layout = get_layout_body()
        result = list(
            SimpleContent.objects.published(
                page, layout
            ).values_list(
                'title', flat=True
            )
        )
        self.assertListEqual(
            ['Hatherleigh Three', 'Jacobstowe One'],
            result
        )

    def test_remove_already(self):
        """content has already been removed and cannot be removed again."""
        c = get_hatherleigh_old()
        self.assertRaises(
            ModerateError,
            c.content.set_removed,
            get_user_staff(),
        )

    def test_remove_pending(self):
        """remove pending content."""
        page = get_page_home()
        layout = get_layout_body()
        c = get_hatherleigh_three()
        c.content.set_removed(get_user_staff())
        c.content.save()
        result = [
            c.title for c in SimpleContent.objects.pending(page, layout)
        ]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_remove_published(self):
        """remove pending content."""
        page = get_page_home()
        layout = get_layout_body()
        c = get_hatherleigh_two()
        c.content.set_removed(get_user_staff())
        c.content.save()
        result = [
            c.title for c in SimpleContent.objects.published(page, layout)
        ]
        self.assertListEqual(
            ['Jacobstowe One',],
            result
        )

    def test_pending_set(self):
        """edit published content."""
        c = get_jacobstowe_one()
        c.title = 'Jacobstowe Edit'
        c.content.set_pending(get_user_staff())
        c.save()
        page = get_page_home()
        layout = get_layout_body()
        result = [c.title for c in SimpleContent.objects.pending(page, layout)]
        self.assertListEqual(
            ['Hatherleigh Three', 'Jacobstowe Edit'],
            result
        )

    def test_pending_when_pending_exists(self):
        """edit published content when content already pending.

        user should not be allowed to edit published content when pending
        content already exists in the section.

        """
        c = get_hatherleigh_two()
        self.assertRaises(
            ModerateError,
            c.content.set_pending,
            get_user_staff()
        )

    def test_pending_when_removed(self):
        """content has been removed, so cannot set to pending."""
        c = get_hatherleigh_old()
        self.assertRaises(
            ModerateError,
            c.content.set_pending,
            get_user_staff()
        )
