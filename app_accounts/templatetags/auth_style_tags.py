from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css_class):
    return field.as_widget(attrs={"class": css_class})

