from django.conf import settings
from urllib.parse import urljoin


def get_full_url(image):
    """
    params: image - instance of ImageField
    """
    if not image:
        return None
    return urljoin(settings.SITE_URL, image.url)
