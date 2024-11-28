from django import template

register = template.Library()

@register.filter
def calculate_progress(completed, target):
    print(f"calculate_progress called with completed={completed}, target={target}")
    if target > 0:
        return round((completed / target) * 100)
    return 0

