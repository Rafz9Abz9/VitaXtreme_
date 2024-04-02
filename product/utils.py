from PIL import Image as PilImage
from django.core.exceptions import ValidationError
from django.template.defaulttags import register


@register.filter(name='order_by_date')
def order_by_date(list):
    return list.order_by('-created_at')


@register.filter(name='remove_slashes')
def remove_slashes(value):
    if value:
        return value.strip('/')
    return value


@register.filter
def get_name(dictionary):
    return dictionary.name


@register.filter
def friendly_name(dictionary):
    return dictionary.friendly_name


@register.filter
def access_list(list, accessor):
    return list[accessor]


@register.filter
def image_url(img_object):
    return img_object.image_file.url


@register.filter
def image_caption(img_object):
    return img_object.caption


@register.filter
def divide_by(number, divider):
    return number / divider


@register.filter
def multiply_by(number, multiplier):
    return number * multiplier


def validate_image_content(value):
    try:
        img = PilImage.open(value)
    except PilImage.UnidentifiedImageError:
        raise ValidationError("File is not a valid image.")
