from django import template

register = template.Library()


@register.inclusion_tag('navbar/sidebar_menu.html')
def get_navbar(section):
    return {'section': section}