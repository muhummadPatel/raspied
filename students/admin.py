from django.contrib import admin

from .models import WhitelistedUsername


class WhitelistedUsernameAdmin(admin.ModelAdmin):
    pass


admin.site.register(WhitelistedUsername, WhitelistedUsernameAdmin)
