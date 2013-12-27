from django.db import models

import reversion

from base.model_utils import TimeStampedModel


def _default_moderate_state():
    return ModerateState.pending()


class ModerateState(models.Model):
    """Accept, remove or pending.

    Copy of class in `story.models'.

    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Moderate'
        verbose_name_plural = 'Moderated'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    @staticmethod
    def pending():
        return ModerateState.objects.get(slug='pending')

    @staticmethod
    def published():
        return ModerateState.objects.get(slug='published')

    @staticmethod
    def removed():
        return ModerateState.objects.get(slug='removed')

reversion.register(ModerateState)


class Section(models.Model):
    """Which part of the web site/page"""
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Section)


class Simple(TimeStampedModel):
    """Simple section.

    TODO I cannot get the migration working for adding the 'moderate_state',
    so have added 'blank' and 'null' for now.

    """
    section = models.ForeignKey(Section)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    moderate_state = models.ForeignKey(
        ModerateState,
        blank=True,
        null=True,
        default=_default_moderate_state
    )

    class Meta:
        ordering = ['section', 'order', 'modified']
        verbose_name = 'Story'
        verbose_name_plural = 'Simple Story'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

    def set_removed(self):
        self.moderate_state = ModerateState.removed()

reversion.register(Simple)
