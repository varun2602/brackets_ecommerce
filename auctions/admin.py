from django.contrib import admin
from . import models
from django.contrib.sessions.models import Session

# Register your models here.
admin.site.register(models.Listing)
admin.site.register(models.User)
admin.site.register(models.Bid)
admin.site.register(models.Comment)
admin.site.register(models.watchlist)
admin.site.register(Session)
# Test comment