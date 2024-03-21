from django import template

register = template.Library()

@register.filter
def likes_summary(users):
    users = list(users)
    if len(users) > 10:
        return ', '.join(str(user) for user in users[:10]) + ' +{} more'.format(len(users) - 10)
    else:
        return ', '.join(str(user) for user in users)