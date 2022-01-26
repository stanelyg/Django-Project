from django.template.defaultfilters import register
@register.filter(name='dic_lookup')
def dic_lookup(d,k,):
    '''Returns the given key from a dictionary.'''
    value=0
    if k in d:
        value+=d[k]

    return value