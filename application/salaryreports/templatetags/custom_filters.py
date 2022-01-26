from django.template import Library
import  datetime
register = Library()

@register.filter
def dict_lookup(d, key):
    if key in d:
        return d[key]
    else:
        return 0
@register.filter
def id_lookup(d,key_list):
    return d[key_list[0]]
@register.filter
def weekly_hours_bg_color(data,wk_date):
    if  str(wk_date)[:-1]=='Hours Worked':
        return data[str(wk_date)+'c']
@register.filter
def analysis_lookup(d,key_list):
    if d !=0:
        if key_list in d:
            return d[key_list]
        else:
            return 0
    else:
        return 0
@register.filter
def monthtextual(value):
    return datetime.date(2020, value, 1).strftime('%B')
