from django import template
from store.models import MyLogo, MyFavicon

register = template.Library()

@register.filter
def logo(user):
    if user.is_authenticated:
        logo = MyLogo.objects.filter(user=user, is_active=True).order_by('-id').first()
        if logo is None:
            return ""
        return logo.image.url

    else:
        logo = MyLogo.objects.filter(is_active=True).order_by('-id').first()
        if logo is None:
            return ""
        return logo.image.url

@register.filter
def favicon(user):
    if user.is_authenticated:
        logo = MyFavicon.objects.filter(user=user, is_active=True).order_by('-id').frist()
        return logo.image.url