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
        return self.model.objects.filter(
            page=page,
        ).order_by(
            'order'
        )

    def published(self, page):
        return self.model.objects.filter(
            page=page,
            moderate_state=ModerateState.published(),
        ).order_by(
            'order'
        )


class Section(TimeStampedModel):
    """Simple section on a web page."""
    page = models.ForeignKey(Page)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    moderate_state = models.ForeignKey(
        ModerateState,
        default=_default_moderate_state
    )
    objects = SectionManager()

    class Meta:
        ordering = ['page', 'order', 'modified']
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

    def set_pending(self):
        self.moderate_state = ModerateState.pending()

    def set_published(self):
        self.moderate_state = ModerateState.published()

    def set_removed(self):
        self.moderate_state = ModerateState.removed()

    def _pending(self):
        return self.moderate_state == ModerateState.pending()
    pending = property(_pending)

    def _published(self):
        return self.moderate_state == ModerateState.published()
    published = property(_published)

reversion.register(Section)
