from django.contrib import admin

from .models import (
    Layout,
    Page,
    Section,
)


class LayoutAdmin(admin.ModelAdmin):
    pass

admin.site.register(Layout, LayoutAdmin)


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('page',)

admin.site.register(Section, SectionAdmin)
