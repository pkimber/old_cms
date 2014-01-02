from django.db import IntegrityError
from django.db import models
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    Content,
)
from cms.tests.scenario import (
    default_scenario_cms,
    get_content_hatherleigh_old,
    get_content_hatherleigh_three,
    get_content_hatherleigh_two,
    get_content_jacobstowe_one,
    get_page_home,
    get_container_hatherleigh_two,
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
        self.assertTrue(get_content_hatherleigh_three().is_pending)

    def test_is_published(self):
        self.assertTrue(get_content_hatherleigh_two().is_published)

    def test_is_removed(self):
        self.assertTrue(get_content_hatherleigh_old().is_removed)

    def test_two_pending_error(self):
        container = get_container_hatherleigh_two()
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            Content(
                container=container,
                moderate_state=ModerateState.pending(),
                title='Hatherleigh 2',
            )
        )

    def test_published(self):
        page = get_page_home()
        result = [c.title for c in Content.objects.published(page=page)]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_pending(self):
        page = get_page_home()
        result = [c.title for c in Content.objects.pending(page=page)]
        self.assertListEqual(
            ['Hatherleigh Three', 'Jacobstowe One'],
            result
        )

    def test_publish_not_pending(self):
        """This content is not 'pending' so cannot be published."""
        content = get_content_hatherleigh_two()
        self.assertRaises(
            ModerateError,
            content.publish,
            get_user_staff(),
        )

    def test_publish(self):
        content = get_content_hatherleigh_three()
        content.publish(get_user_staff())
        content.save()
        page = get_page_home()
        result = list(
            Content.objects.published(
                page=page
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
        content = get_content_hatherleigh_old()
        self.assertRaises(
            ModerateError,
            content.remove,
            get_user_staff(),
        )

    def test_remove_pending(self):
        """remove pending content."""
        page = get_page_home()
        content = get_content_hatherleigh_three()
        content.remove(get_user_staff())
        content.save()
        result = [c.title for c in Content.objects.pending(page=page)]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_remove_published(self):
        """remove pending content."""
        page = get_page_home()
        content = get_content_hatherleigh_two()
        content.remove(get_user_staff())
        content.save()
        result = [c.title for c in Content.objects.published(page=page)]
        self.assertListEqual(
            ['Jacobstowe One',],
            result
        )

    def test_pending_set(self):
        """edit published content."""
        content = get_content_jacobstowe_one()
        content.title = 'Jacobstowe Edit'
        content.pending(get_user_staff())
        content.save()
        page = get_page_home()
        result = [c.title for c in Content.objects.pending(page=page)]
        self.assertListEqual(
            ['Hatherleigh Three', 'Jacobstowe Edit'],
            result
        )

    def test_pending_when_pending_exists(self):
        """edit published content when content already pending.

        user should not be allowed to edit published content when pending
        content already exists in the section.

        """
        content = get_content_hatherleigh_two()
        self.assertRaises(
            ModerateError,
            content.pending,
            get_user_staff()
        )

    def test_pending_when_removed(self):
        """content has been removed, so cannot set to pending."""
        content = get_content_hatherleigh_old()
        self.assertRaises(
            ModerateError,
            content.pending,
            get_user_staff()
        )
