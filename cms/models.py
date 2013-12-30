from django.db import models
from django.db.models import Q

import reversion

from base.model_utils import TimeStampedModel
from moderate.models import ModerateModel


class Page(models.Model):
    """Which page on the web site."""
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Page)


class SectionManager(models.Manager):

    def pending(self, page):
        published = ModerateState.published()
        pending = ModerateState.pending()
        sections = self.model.objects.filter(
            page=page,
            moderate_state__in=[published, pending],
        ).order_by(
            'order',
            'moderate_state__slug',
        )
        previous = None
        result = []
        for section in sections:
            if previous and section.order == previous:
                pass
            else:
                result.append(section)
            previous = section.order
        return result

    def published(self, page):
        return self.model.objects.filter(
            page=page,
            moderate_state=ModerateState.published(),
        ).order_by(
            'order'
        )


class Section(ModerateModel, TimeStampedModel):
    """Simple section on a web page."""
    page = models.ForeignKey(Page)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    objects = SectionManager()

    class Meta:
        ordering = ['page', 'order', 'modified']
        unique_together = ('page', 'order', 'moderate_state')
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

reversion.register(Section)
