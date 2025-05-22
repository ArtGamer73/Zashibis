from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png'))

@register.filter
def is_video(file_url):
    return file_url.lower().endswith(('.mp4', '.webm'))