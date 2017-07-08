from django import template

register = template.Library()

@register.inclusion_tag('posts/includes/ad_post_card.html')
def paste_ad(ad):
    return { 'ad': ad }