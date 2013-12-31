from django.contrib import admin

from .models import (
    Page,
    Section,
    Content,
)


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)


class ContentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Content, ContentAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('page',)

admin.site.register(Section, SectionAdmin)
