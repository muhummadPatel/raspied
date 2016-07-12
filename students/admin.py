from django.contrib import admin

from .models import WhitelistedUsername


@admin.register(WhitelistedUsername)
class WhitelistedUsernameAdmin(admin.ModelAdmin):
    pass
