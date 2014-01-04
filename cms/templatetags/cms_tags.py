from django import template


register = template.Library()


@register.inclusion_tag('cms/_moderate.html')
def cms_moderate(content):
    return dict(content=content)
