from django import template

register = template.Library()
@register.filter
def std_tag_msg(tag):
    if tag == "error":
        return "danger"
    return tag
@register.filter
def std_tag_icons(tag):
    if tag == "error":
        return '<i class="dripicons-wrong me-2"></i>'
    elif tag == "success":
        return '<i class="dripicons-checkmark me-2"></i>'
    elif tag == "warning":
        return '<i class="dripicons-warning me-2"></i>'
    else:
        return '<i class="dripicons-information me-2"></i>'

