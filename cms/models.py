import collections

from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q

import reversion

from base.model_utils import TimeStampedModel


def default_moderate_state():
    return ModerateState.pending()


class CmsError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class ModerateState(models.Model):
    """Accept, remove or pending."""
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


class PageManager(models.Manager):

    def menu(self):
        """Return page objects for a menu."""
        return self.model.objects.all().order_by('order')


class Page(TimeStampedModel):
    """Which page on the web site.

    An order of zero (0) indicates that the page should be excluded from a
    menu.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    is_home = models.BooleanField(default=False)
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

    def next_order(self):
        qs = self.container_set.all().order_by(
            '-order'
        )[:1]
        if qs:
            return qs[0].order + 1
        else:
            return 1

reversion.register(Section)


class Container(TimeStampedModel):
    """Manage one piece of content which can be in various states.

    e.g. pending, published and removed.

    """
    section = models.ForeignKey(Section)
    # TODO I am not sure we need 'order' on this model at all.  The 'order' of
    # an object should probably be the responsibility of the content object.
    # In fact, in some cases the ordering might be by something else e.g. date.
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'

    def __unicode__(self):
        return unicode('{}'.format(self.section.page.name))

reversion.register(Container)


class ContentManager(models.Manager):

    def pending(self, section, kwargs=None):
        """Return a list of pending content for a section.

        Note: we return a list of content instances not a queryset.

        """
        pending = ModerateState.pending()
        published = ModerateState.published()
        qs = self.model.objects.filter(
            container__section=section,
            moderate_state__in=[published, pending],
        )
        if kwargs:
            qs = qs.filter(**kwargs)
        qs = qs.order_by('container__order')
        result = collections.OrderedDict()
        for c in qs:
            if c.container.pk in result:
                if c.moderate_state == pending:
                    result[c.container.pk] = c
            else:
                result[c.container.pk] = c
        return result.values()

    def published(self, section):
        """Return a published content for a page."""
        published = ModerateState.published()
        return self.model.objects.filter(
            container__section=section,
            moderate_state=published,
        ).order_by(
            'container__order',
        )


class ContentModel(TimeStampedModel):
    container = models.ForeignKey(Container)
    moderate_state = models.ForeignKey(
        ModerateState,
        default=default_moderate_state
    )
    date_moderated = models.DateTimeField(blank=True, null=True)
    user_moderated = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    objects = ContentManager()

    class Meta:
        abstract = True
        ordering = ['container__section__page__name', 'order', 'moderate_state__slug']
        verbose_name = 'Content'
        verbose_name_plural = 'Content'

    def __unicode__(self):
        return unicode('{}: {}, order {}'.format(self.pk, self.moderate_state, self.order))

    def _delete_removed_content(self):
        """delete content which was previously removed."""
        try:
            c = self._get_content_set().get(
                moderate_state=ModerateState.removed()
            )
            c.delete()
        except self.DoesNotExist:
            pass

    def _get_content_set(self):
        raise CmsError(
            "Concrete class must implement the '_get_content_set' method"
        )

    def _is_pending(self):
        return self.moderate_state == ModerateState.pending()
    is_pending = property(_is_pending)

    def _is_published(self):
        return self.moderate_state == ModerateState.published()
    is_published = property(_is_published)

    def _is_removed(self):
        return self.moderate_state == ModerateState.removed()
    is_removed = property(_is_removed)

    def _set_moderated(self, user, moderate_state):
        self.date_moderated = datetime.now()
        self.user_moderated = user
        self.moderate_state = moderate_state

    def _set_published_to_remove(self, user):
        """publishing new content, so remove currently published content."""
        try:
            c = self._get_content_set().get(
                moderate_state=ModerateState.published()
            )
            c.set_removed(user)
            c.save()
        except self.DoesNotExist:
            pass

    def set_pending(self, user):
        if self.moderate_state == ModerateState.published():
            try:
                self._get_content_set().get(
                    moderate_state=ModerateState.pending()
                )
                raise CmsError(
                    "Section already has pending content so "
                    "published content should not be edited."
                )
            except self.DoesNotExist:
                self._set_moderated(user, ModerateState.pending())
                self.pk = None
        elif self.moderate_state == ModerateState.pending():
            return
        else:
            raise CmsError(
                "Cannot edit content which has been removed"
            )

    def set_published(self, user):
        """Publish content."""
        if not self.moderate_state == ModerateState.pending():
            raise CmsError(
                "Cannot publish content unless it is 'pending'"
            )
        self._delete_removed_content()
        self._set_published_to_remove(user)
        self._set_moderated(user, ModerateState.published())

    def set_removed(self, user):
        """Remove content."""
        if self.moderate_state == ModerateState.removed():
            raise CmsError(
                "Cannot remove content which has already been removed"
            )
        self._delete_removed_content()
        self._set_moderated(user, ModerateState.removed())

    def url_publish(self):
        raise CmsError("class must implement 'url_publish' method")

    def url_remove(self):
        raise CmsError("class must implement 'url_remove' method")

    def url_update(self):
        raise CmsError("class must implement 'url_update' method")
