from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

register = template.Library()


SVG_TEMPLATE = '<svg{}>{}<use href="{}#{}"/></svg>'


@register.simple_tag
def svg_sprite(id_, title=None, **kwargs):
    try:
        sprite = settings.SVG_SPRITE
    except AttributeError:
        raise ImproperlyConfigured('SVG_SPRITE setting missing')

    title_tag = format_html('<title>{}</title>', title) if title else ''
    attributes = format_html_join('', ' {}="{}"', kwargs.items())
    path = static(sprite)
    return format_html(SVG_TEMPLATE, attributes, title_tag, path, id_)
