from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def highlights(context):
    user = context['request'].user
    narratives = user.narratives.all()
    highlights = narratives[:5]
    return highlights