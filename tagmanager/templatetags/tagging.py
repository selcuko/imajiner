from django import template

register = template.Library()

@register.simple_tag(name='tags_for_user', takes_context=True)
def narrative_tags_for_user(context, count=10):
    narrative = context['narrative']
    user = context['request'].user
    return narrative.tags.for_user(user)