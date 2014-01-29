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
    Layout,
    Page,
    Section,
)


class ContentPageMixin(BaseMixin):
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


class ContentCreateView(ContentPageMixin, BaseMixin, CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # create a new container for the content
        section = self.get_section()
        container = Container(section=section, order=section.next_order())
        container.save()
        self.object.container = container
        return super(ContentCreateView, self).form_valid(form)

    def get_success_url(self):
        page = self.get_page()
        return reverse(
            'project.page.design',
            kwargs=dict(page=page.slug)
        )


class ContentPublishView(BaseMixin, UpdateView):

    def form_valid(self, form):
        """Publish 'pending' content."""
        self.object = form.save(commit=False)
        self.object.set_published(self.request.user)
        messages.info(
            self.request,
            "Published content, id {}".format(
                self.object.pk,
            )
        )
        return super(ContentPublishView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'project.page.design',
            kwargs=dict(page=self.object.container.section.page.slug)
        )


class ContentRemoveView(BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_removed(self.request.user)
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
            kwargs=dict(page=self.object.container.section.page.slug)
        )


class ContentUpdateView(BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_pending(self.request.user)
        return super(ContentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'project.page.design',
            kwargs=dict(page=self.object.container.section.page.slug)
        )
