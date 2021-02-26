
from django.contrib import admin

from .models import UserProfile, Organizations, License, Entitlement

admin.site.register(UserProfile)

admin.site.register(Organizations)

admin.site.register(Entitlement)

admin.site.register(License)