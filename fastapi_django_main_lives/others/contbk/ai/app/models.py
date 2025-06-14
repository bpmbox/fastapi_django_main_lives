from django.db import models

class WebSite(models.Model):
    url = models.URLField(unique=True)
    data = models.TextField(blank=True)

    def __str__(self):
        return self.url