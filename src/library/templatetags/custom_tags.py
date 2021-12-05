from django import template

register = template.Library()


@register.filter('join_link')
def join_link(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for i in value:
        arr.append('<a href="%s">%s</a>' % (
            i.get_absolute_url(), conditional_escape(i)
        ))

    return arg.join(arr)
