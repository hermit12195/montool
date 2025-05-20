from django.contrib import admin

from app import models

admin.site.register(models.MonUser)
admin.site.register(models.Server)
admin.site.register(models.Profile)
