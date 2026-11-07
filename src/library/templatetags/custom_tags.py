from django import template
from library.models import BookInstance, MaterialInstance

register = template.Library()


@register.filter('join_link')
def join_link(value, arg):
    """
    Joins the items of value as link to itself together using arg

    The item in values are properly escaped so the safe filter can be applied
    Example usage:
    {%  book.author.all|join_link:", " % | safe}
    """
    from django.utils.html import conditional_escape
    arr = []
    for i in value:
        arr.append('<a href="%s">%s</a>' % (
            i.get_absolute_url(), conditional_escape(i)
        ))

    return arg.join(arr)


@register.filter
def get_type(value):
    return type(value)


@register.filter
def is_bookinstance(value):
    return type(value) == BookInstance


@register.filter
def is_materialinstance(value):
    return type(value) == MaterialInstance


@register.simple_tag(takes_context=True)
def var_exists(context, name):
    dicts = context.dicts  # array of dicts
    if dicts:
        for d in dicts:
            if name in d:
                return True
    return False


@register.filter
def dir(value):
    return value.__dir__()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()



@register.filter
def ellided_range(page_obj, page_number):
    return page_obj.paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)