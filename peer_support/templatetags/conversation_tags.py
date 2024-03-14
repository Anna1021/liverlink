from django import template
import time

register = template.Library()

@register.simple_tag
def sender_if_applicable(message,user,conversation):
    if conversation.as_group() is None:
        return ""
    previous = message.previous_message
    while previous is not None and user not in previous.visible_to.all():
        previous = previous.previous_message
    if previous is not None and previous.sender==message.sender:
        return ""
    return message.sender.username

@register.simple_tag
def conversation_name(user,conversation):
    if conversation.as_group() is not None:
        return str(conversation.as_group())
    other_user = conversation.users.exclude(pk=user.pk)[0]
    return other_user.username

@register.filter
def visible_messages(user,conversation):
    return conversation.messages.filter(visible_to__in=[user])