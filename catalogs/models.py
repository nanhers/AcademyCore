from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class ClientStatus(models.Model):
    """Model to represent the status of a client (Active, Inactive, Temporarily Inactive)."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Client Status")  # Nombre en singular
        verbose_name_plural = _("Client Statuses")  # Nombre en plural

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Model to represent subscriptions."""
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=150, verbose_name=_("Name"))

    def __str__(self):
        return f"{self.name} ({self.code})"


class DiscoverySource(models.Model):
    """Model to represent discovery sources."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name
