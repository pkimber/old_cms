# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

import reversion

from cms.models import ContentModel


class TestContent(ContentModel):

    title = models.TextField()

    class Meta:
        # cannot put 'unique_together' on abstract base class
        # https://code.djangoproject.com/ticket/16732
        unique_together = ('container', 'moderate_state')
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def _get_content_set(self):
        return self.container.testcontent_set

    def __str__(self):
        return '{} {}'.format(self.title, self.moderate_state)

    def url_publish(self):
        return reverse('example.test.publish', kwargs={'pk': self.pk})

    def url_remove(self):
        return reverse('example.test.remove', kwargs={'pk': self.pk})

    def url_update(self):
        return reverse('example.test.update', kwargs={'pk': self.pk})

reversion.register(TestContent)
