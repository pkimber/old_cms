from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
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

    model = Content

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # create a new container for this content
        section = self.get_section()
        container = Container(section=section)
        container.save()
        # init our new content object
        self.object.container = container
        self.object.order = Content.objects.next_order(container.section)
        return super(ContentCreateView, self).form_valid(form)


class ContentPublishView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = Content

    def form_valid(self, form):
        """Publish 'pending' content."""
        self.object = form.save(commit=False)
        self.object.publish(self.request.user)
        messages.info(
            self.request,
            "Published content {}, {}".format(
                self.object.pk,
                self.object.title,
            )
        )
        return super(ContentPublishView, self).form_valid(form)


class ContentRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = Content

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.remove(self.request.user)
        messages.info(
            self.request,
            "Removed content {}, {}".format(
                self.object.pk,
                self.object.title,
            )
        )
        return super(ContentRemoveView, self).form_valid(form)


class ContentUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = Content

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.pending(self.request.user)
        return super(ContentUpdateView, self).form_valid(form)
