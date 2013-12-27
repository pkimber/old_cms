from django.contrib import admin

from .models import (
    Page,
    Section,
)


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'order', 'title', 'moderate_state')

admin.site.register(Section, SectionAdmin)
