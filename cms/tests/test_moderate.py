from django.db import IntegrityError
from django.db import models
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from cms.models import (
    Page,
    Section,
    Content,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)
from moderate.models import (
    ModerateError,
    ModerateState,
)
from moderate.tests.scenario import create_default_moderate_state


class TestModerate(TestCase):

    def setUp(self):
        create_default_moderate_state()
        default_scenario_login()
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
        self.hatherleigh_one = clean_and_save(
            Content(
                section=self.section,
                order=1,
                moderate_state=ModerateState.pending(),
                title='Hatherleigh One',
            )
        )
        self.hatherleigh_two = clean_and_save(
            Content(
                section=self.section,
                order=1,
                moderate_state=ModerateState.published(),
                title='Hatherleigh Two',
            )
        )
        self.hatherleigh_old = clean_and_save(
            Content(
                section=self.section,
                order=3,
                moderate_state=ModerateState.removed(),
                title='Hatherleigh Old',
            )
        )
        # Jacobstowe
        section2 = clean_and_save(
            Section(
                page=self.page,
            )
        )
        self.jacobstowe_one = clean_and_save(
            Content(
                section=section2,
                order=2,
                moderate_state=ModerateState.published(),
                title='Jacobstowe One',
            )
        )

    def test_two_pending_error(self):
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            Content(
                section=self.section,
                moderate_state=ModerateState.pending(),
                title='Hatherleigh 2',
            )
        )

    def test_published(self):
        result = [c.title for c in Content.objects.published(page=self.page)]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_pending(self):
        result = [c.title for c in Content.objects.pending(page=self.page)]
        self.assertListEqual(
            ['Hatherleigh One', 'Jacobstowe One'],
            result
        )

    def test_publish_not_pending(self):
        """This content is not 'pending' so cannot be published."""
        self.assertRaises(
            ModerateError,
            self.hatherleigh_two.publish,
            get_user_staff(),
        )

    def test_publish(self):
        self.hatherleigh_one.publish(get_user_staff())
        self.hatherleigh_one.save()
        result = list(
            Content.objects.published(
                page=self.page
            ).values_list(
                'title', flat=True
            )
        )
        self.assertListEqual(
            ['Hatherleigh One', 'Jacobstowe One'],
            result
        )

    def test_remove_already(self):
        """content has already been removed and cannot be removed again."""
        self.assertRaises(
            ModerateError,
            self.hatherleigh_old.remove,
            get_user_staff(),
        )

    def test_remove_pending(self):
        """remove pending content."""
        self.hatherleigh_one.remove(get_user_staff())
        self.hatherleigh_one.save()
        result = [c.title for c in Content.objects.pending(page=self.page)]
        self.assertListEqual(
            ['Hatherleigh Two', 'Jacobstowe One'],
            result
        )

    def test_remove_published(self):
        """remove pending content."""
        self.hatherleigh_two.remove(get_user_staff())
        self.hatherleigh_two.save()
        result = [c.title for c in Content.objects.published(page=self.page)]
        self.assertListEqual(
            ['Jacobstowe One',],
            result
        )

    def test_set_pending(self):
        """edit published content."""
        self.jacobstowe_one.title = 'Jacobstowe Edit'
        self.jacobstowe_one.set_pending(get_user_staff())
        self.jacobstowe_one.save()
        result = [c.title for c in Content.objects.pending(page=self.page)]
        self.assertListEqual(
            ['Hatherleigh One', 'Jacobstowe Edit'],
            result
        )

    def test_set_pending_when_pending_exists(self):
        """edit published content when content already pending.

        user should not be allowed to edit published content when pending
        content already exists in the section.

        """
        self.assertRaises(
            ModerateError,
            self.hatherleigh_two.set_pending,
            get_user_staff()
        )

    def test_set_pending_when_removed(self):
        """content has been removed, so cannot set to pending."""
        self.assertRaises(
            ModerateError,
            self.hatherleigh_old.set_pending,
            get_user_staff()
        )
