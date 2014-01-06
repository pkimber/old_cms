from django import template


register = template.Library()


@register.inclusion_tag('cms/_add.html')
def cms_add(url):
    return dict(url=url)


@register.inclusion_tag('cms/_moderate.html')
def cms_moderate(generic_content, can_remove=True):
    return dict(c=generic_content, can_remove=can_remove)
