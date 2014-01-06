from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin
from cms.models import (
    CmsError,
    Container,
    Content,
    Layout,
    Page,
    Section,
)


class ContentPageMixin(object):
    """Page information."""

    def get_context_data(self, **kwargs):
        context = super(ContentPageMixin, self).get_context_data(**kwargs)
        context.update(dict(
            page=self.get_page(),
            pages=Page.objects.menu(),
        ))
        return context

    def get_layout(self):
        layout = self.kwargs.get('layout', None)
        if not layout:
            raise CmsError("no 'layout' parameter in url")
        return get_object_or_404(Layout, slug=layout)

    def get_page(self):
        page = self.kwargs.get('page', None)
        if not page:
            raise CmsError("no 'page' parameter in url")
        return get_object_or_404(Page, slug=page)

    def get_section(self):
        return get_object_or_404(
            Section,
            page=self.get_page(),
            layout=self.get_layout()
        )


class ContentCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin,
        ContentPageMixin, BaseMixin, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # create a new container for the content
        section = self.get_section()
        container = Container(section=section)
        container.save()
        # create a new content object for the ...
        content = Content(container=container)
        content.order = Content.objects.next_order(section)
        content.save()
        # init our object (one to one relation to content)
        self.object.content = content
        return super(ContentCreateView, self).form_valid(form)

    def get_success_url(self):
        page = self.get_page()
        return reverse(
            'project.page.design',
            kwargs=dict(page=page.slug)
        )


class ContentPublishView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        """Publish 'pending' content."""
        self.object = form.save(commit=False)
        self.object.content.set_published(self.request.user)
        self.object.content.save()
        messages.info(
            self.request,
            "Published content {}, {}".format(
                self.object.pk,
                self.object.title,
            )
        )
        return super(ContentPublishView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'project.page.design',
            kwargs=dict(page=self.object.content.container.section.page.slug)
        )


class ContentRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content.set_removed(self.request.user)
        self.object.content.save()
        messages.info(
            self.request,
            "Removed content {}, {}".format(
                self.object.pk,
                self.object.title,
            )
        )
        return super(ContentRemoveView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'project.page.design',
            kwargs=dict(page=self.object.content.container.section.page.slug)
        )


class ContentUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        content = self.object.content
        content.set_pending(self.request.user)
        is_new_content = not content.pk
        if is_new_content:
            self.object.pk = None
        content.save()
        if is_new_content:
            self.object.content = content
        #import ipdb
        #ipdb.set_trace()
        #self.object.content.set_pending(self.request.user)
        #if not self.object.content.pk:
        #    self.object.pk = None
        #self.object.content.save()
        #self.object.content = temp
        return super(ContentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'project.page.design',
            kwargs=dict(page=self.object.content.container.section.page.slug)
        )
