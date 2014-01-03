from django.db import models
from django.db.models import Q

import reversion

from base.model_utils import TimeStampedModel
from moderate.models import (
    ModerateError,
    ModerateModel,
    ModerateState,
)


class CmsError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))



class PageManager(models.Manager):

    def menu(self):
        """Return page objects for a menu."""
        return self.model.objects.filter(
            order__gt=0
        ).order_by(
            'order'
        )


class Page(TimeStampedModel):
    """Which page on the web site.

    An order of zero (0) indicates that the page should be excluded from a
    menu.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    objects = PageManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Page)


class Layout(TimeStampedModel):
    """Layout area e.g. content, header, footer."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Layout'
        verbose_name_plural = 'Layout'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Layout)


class Section(TimeStampedModel):
    """Section of a web page e.g. content, header, footer."""
    page = models.ForeignKey(Page)
    layout = models.ForeignKey(Layout)

    class Meta:
        ordering = ['page', 'modified']
        unique_together = ('page', 'layout')
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return unicode('{}'.format(self.page.name))

reversion.register(Section)


class Container(TimeStampedModel):
    """Manage one piece of content which can be in various states.

    e.g. pending, published and removed.

    """
    section = models.ForeignKey(Section)

    class Meta:
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'

    def __unicode__(self):
        return unicode('{}'.format(self.section.page.name))

reversion.register(Container)


class ContentManager(models.Manager):

    def next_order(self, section):
        content = self.model.objects.filter(
            container__section=section,
        ).order_by(
            '-order'
        )[:1]
        if content:
            return content[0].order + 1
        else:
            return 1

    def pending(self, page, layout):
        """Return a list of pending content for a page.

        Note: we return a list of content not a queryset.

        """
        pending = ModerateState.pending()
        published = ModerateState.published()
        qs = self.model.objects.filter(
            container__section__page=page,
            container__section__layout=layout,
            moderate_state__in=[published, pending],
        ).order_by(
            'order',
        )
        result = {}
        for content in qs:
            if content.container.pk in result:
                if content.moderate_state == pending:
                    result[content.container.pk] = content
            else:
                result[content.container.pk] = content
        return result.values()

    def published(self, page, layout):
        """Return a published content for a page."""
        published = ModerateState.published()
        return self.model.objects.filter(
            container__section__page=page,
            container__section__layout=layout,
            moderate_state=published,
        ).order_by(
            'order',
        )


class Content(ModerateModel, TimeStampedModel):
    """Simple section on a web page."""
    container = models.ForeignKey(Container)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    objects = ContentManager()

    class Meta:
        ordering = ['section__page__name', 'order', 'moderate_state__slug']
        unique_together = ('container', 'moderate_state')
        verbose_name = 'Content'
        verbose_name_plural = 'Content'

    def __unicode__(self):
        return unicode('{} {}'.format(self.title, self.moderate_state))

    def _delete_removed_content(self):
        """delete content which was previously removed."""
        try:
            content = self.container.content_set.get(
                moderate_state=ModerateState.removed()
            )
            content.delete()
        except Content.DoesNotExist:
            pass

    def _set_published_to_remove(self, user):
        """publishing new content, so remove currently published content."""
        try:
            content = self.container.content_set.get(
                moderate_state=ModerateState.published()
            )
            content.set_removed(user)
            content.save()
        except Content.DoesNotExist:
            pass

    def pending(self, user):
        if self.moderate_state == ModerateState.published():
            try:
                self.container.content_set.get(
                    moderate_state=ModerateState.pending()
                )
                raise ModerateError(
                    "Section already has pending content so "
                    "published content should not be edited."
                )
            except Content.DoesNotExist:
                self.set_pending(user)
                self.pk = None
        elif self.moderate_state == ModerateState.pending():
            return
        else:
            raise ModerateError(
                "Cannot edit content which has been removed"
            )

    def publish(self, user):
        """Publish content."""
        if not self.moderate_state == ModerateState.pending():
            raise ModerateError(
                "Cannot publish content unless it is 'pending'"
            )
        self._delete_removed_content()
        self._set_published_to_remove(user)
        self.set_published(user)

    def remove(self, user):
        """Remove content."""
        if self.moderate_state == ModerateState.removed():
            raise ModerateError(
                "Cannot remove content which has already been removed"
            )
        self._delete_removed_content()
        self.set_removed(user)

reversion.register(Content)
