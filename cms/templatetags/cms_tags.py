from django import template


register = template.Library()


@register.inclusion_tag('cms/_add.html')
def cms_add(page_slug, layout_slug):
    return dict(
        page_slug=page_slug,
        layout_slug=layout_slug,
    )


@register.inclusion_tag('cms/_moderate.html')
def cms_moderate(generic_content):
    return dict(generic_content=generic_content)
