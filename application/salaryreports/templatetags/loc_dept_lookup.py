from django.template import Library
register = Library()
@register.filter
def loc_dept_lookup(d,key):
    if key in d:
        for value_key in d[key]:
           return d[key][value_key]
    else:
        return 0
