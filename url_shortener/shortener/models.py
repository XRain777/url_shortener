from django.db import models
from .base58 import base_decode, base_encode

SQLITE_MAX_INT = 9223372036854775807

class LinkManager(models.Manager):
    def have_short_url(self, short_url):
        try:
            url_pk = base_decode(short_url)
        except KeyError:
            return super().get_queryset().none()
        if url_pk <= SQLITE_MAX_INT:
            return super().get_queryset().filter(pk=url_pk)
        else:
            return super().get_queryset().none()

class Link(models.Model):
    url = models.URLField(max_length=2048)
    click_count = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField()
    objects = LinkManager()

    def short_url(self):
        return base_encode(self.pk)