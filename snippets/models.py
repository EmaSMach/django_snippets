from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="snippets")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    snippet = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=False, blank=False, related_name="snippets")

    def __str__(self):
        return self.name
