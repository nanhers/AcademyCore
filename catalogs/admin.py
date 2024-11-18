from django.contrib import admin
from .models import ClientStatus, Subscription, DiscoverySource

# Register your models here.
admin.site.register(ClientStatus)
admin.site.register(Subscription)
admin.site.register(DiscoverySource)