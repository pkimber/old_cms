from django.core.exceptions import ImproperlyConfigured
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
    Content,
    Section,
)


class ContentCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    model = Content

    def get_page(self):
        raise ImproperlyConfigured(
            "{} is missing a 'get_page' method.".format(
                self.__class__.__name__
            )
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        page = self.get_page()
        # create a new section for this content
        section = Section(page=page)
        section.save()
        # init our new content object
        self.object.section = section
        self.object.order = Content.objects.next_order(page)
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
