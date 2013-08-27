from django.contrib import admin

from .models import Section, Simple


class SectionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)


class SimpleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Simple, SimpleAdmin)
