from django import template

register = template.Library()

@register.filter(name='status_color')
def status_color(value, *args):
    return_value = ""
    color_map = {10:"FF0000", 9:"FF3300", 8:"ff6600", 7:"ff9900", 
                 6:"FFCC00", 5:"FFFF00", 4:"ccff00", 3:"99ff00", 
                 2:"66ff00", 1:"33ff00", 0:"00FF00"}
    if value > 10:
        return_value = "ff6600"
    else:
        return_value = (color_map.get(value) or 'fff')
    return return_value