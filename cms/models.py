from django.db import models
from django.db.models import Q

import reversion

from base.model_utils import TimeStampedModel
from moderate.models import (
    ModerateError,
    ModerateModel,
    ModerateState,
)


#class PageManager(models.Manager):
#
#    def published(self, page):
#        import ipdb
#        ipdb.set_trace()
#        return self.model.moderate.published().filter(
#            page=page,
#        ).order_by(
#            'order'
#        )


class Page(models.Model):
    """Which page on the web site."""
    name = models.CharField(max_length=100)
    #objects = PageManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    #def pending(self):
    #    pending = ModerateState.pending()
    #    published = ModerateState.published()
    #    qs = self.section_set.filter(
    #        version__moderate_state__in=[published, pending]
    #    ).order_by(
    #        'order',
    #    )
    #    result = {}
    #    for version in qs:
    #        if version.pk in result:
    #            import ipdb
    #            ipdb.set_trace()
    #            if version.moderate_state == pending:
    #                result[version.pk] = version
    #        else:
    #            result[version.pk] = version
    #    return result.values()

    #def published(self):
    #    published = ModerateState.published()
    #    return self.section_set.filter(
    #        version__moderate_state=published
    #    ).order_by(
    #        'order',
    #    )

reversion.register(Page)


#class SectionManager(models.Manager):
#
#    def pending(self, page):
#        return self.model.moderate.pending().filter(
#            page=page,
#        ).order_by(
#            'order',
#            'moderate_state__slug',
#        )
#
#    def published(self, page):
#        import ipdb
#        ipdb.set_trace()
#        return self.model.moderate.published().filter(
#            page=page,
#        ).order_by(
#            'order'
#        )

#
#    def pending(self, page):
#        published = ModerateState.published()
#        pending = ModerateState.pending()
#        sections = self.model.objects.filter(
#            page=page,
#            moderate_state__in=[published, pending],
#        ).order_by(
#            'order',
#            'moderate_state__slug',
#        )
#        previous = None
#        result = []
#        for section in sections:
#            if previous and section.order == previous:
#                pass
#            else:
#                result.append(section)
#            previous = section.order
#        return result
#
#    def published(self, page):
#        return self.model.objects.filter(
#            page=page,
#            moderate_state=ModerateState.published(),
#        ).order_by(
#            'order'
#        )


class Section(ModerateModel, TimeStampedModel):
    """Simple section on a web page."""
    page = models.ForeignKey(Page)



    #order = models.IntegerField()
    #title = models.TextField()
    #description = models.TextField(blank=True, null=True)
    #picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    #url = models.URLField(blank=True, null=True)
    #objects = SectionManager()
    #objects = models.Manager()

    class Meta:
        ordering = ['page', 'modified']
        # unique_together = ('page', 'order', 'moderate_state')
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return unicode('{} {}'.format(self.page.name, self.order))

reversion.register(Section)


class ContentManager(models.Manager):

    def pending(self, page):
        """Return a list of pending content for a page.

        Note: we return a list of content not a queryset.
        """
        pending = ModerateState.pending()
        published = ModerateState.published()
        qs = self.model.objects.filter(
            section__page=page,
            moderate_state__in=[published, pending],
        ).order_by(
            'order',
        )
        result = {}
        for content in qs:
            if content.section.pk in result:
                if content.moderate_state == pending:
                    result[content.section.pk] = content
            else:
                result[content.section.pk] = content
        return result.values()

    def published(self, page):
        """Return a published content for a page."""
        published = ModerateState.published()
        return self.model.objects.filter(
            section__page=page,
            moderate_state=published,
        ).order_by(
            'order',
        )


class Content(ModerateModel, TimeStampedModel):
    """Simple section on a web page."""
    section = models.ForeignKey(Section)
    order = models.IntegerField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='cms/simple/%Y/%m/%d', blank=True)
    url = models.URLField(blank=True, null=True)
    objects = ContentManager()
    #objects = models.Manager()

    class Meta:
        #ordering = ['page', 'order', 'modified']
        unique_together = ('section', 'moderate_state')
        verbose_name = 'Content'
        verbose_name_plural = 'Content'

    def __unicode__(self):
        return unicode('{} {}'.format(self.title, self.moderate_state))

    def _delete_removed_content(self):
        try:
            content = self.section.content_set.get(
                moderate_state=ModerateState.removed()
            )
            content.delete()
        except Content.DoesNotExist:
            pass

    def _set_published_to_remove(self, user):
        try:
            content = self.section.content_set.get(
                moderate_state=ModerateState.published()
            )
            content._set_removed(user)
            content.save()
        except Content.DoesNotExist:
            pass

    def publish(self, user):
        """Publish this content."""
        if not self.moderate_state == ModerateState.pending():
            raise ModerateError(
                "Cannot publish contene unless it is 'pending'"
            )
        self._delete_removed_content()
        self._set_published_to_remove(user)
        self._set_published(user)
        self.save()

    def remove(self, user):
        """Remove this content."""
        if self.moderate_state == ModerateState.removed():
            raise ModerateError(
                "Cannot remove content which has already been removed"
            )
        self._delete_removed_content()
        self._set_removed(user)
        self.save()

reversion.register(Content)
