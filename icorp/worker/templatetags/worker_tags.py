from django import template

register = template.Library()


@register.inclusion_tag('navbar/sidebar_menu.html')
def get_navbar(section):
    return {'section': section}

@register.simple_tag(name='is_admin_creater_profile')
def is_admin_creater_profile(user):
    return user.groups.filter(name='admin-creater-profile').exists() or user.is_superuser