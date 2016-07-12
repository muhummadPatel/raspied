from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from .models import WhitelistedUsername


@admin.register(WhitelistedUsername)
class WhitelistedUsernameAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(WhitelistedUsernameAdmin, self).get_urls()
        my_urls = [
            url(r'^add/$', self.my_view),
        ]
        return my_urls + urls

    def my_view(self, request):
        # TODO: do this if GET request, and if post, then parse->add the usernames
        context = {
            'opts': WhitelistedUsername._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        }
        return TemplateResponse(request, "students/add_whitelisted_usernames.html", context)
