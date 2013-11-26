from django.db import models

import reversion

from base.model_utils import TimeStampedModel


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
    """ Event """
    section = models.ForeignKey(Section)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ['section', 'order', 'modified']
        verbose_name = 'Story'
        verbose_name_plural = 'Simple Story'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

reversion.register(Simple)
