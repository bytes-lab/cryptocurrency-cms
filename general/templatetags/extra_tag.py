from django import template
from django.contrib.auth.models import Group 
import json

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 


@register.filter
def permitted(user):
    group = user.groups.first()
    return not group.name.lower() in ['translator'] if group else True


@register.filter
def broker(user):
    return user.groups.first().name.lower()
