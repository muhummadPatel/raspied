from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Booking, RobotTerminal, WhitelistedUsername


@admin.register(WhitelistedUsername)
class WhitelistedUsernameAdmin(admin.ModelAdmin):
    """
    Admin class for the WhitelistedUsername model. Handles batch uploading of
    usernames via a text file.
    """

    def get_urls(self):
        urls = super(WhitelistedUsernameAdmin, self).get_urls()
        my_urls = [
            url(r'^add/$', self.add_view),
        ]
        return my_urls + urls

    def add_view(self, request):
        context = {
            'opts': WhitelistedUsername._meta,
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        }

        if request.method == 'GET':
            return TemplateResponse(request, 'students/add_whitelisted_usernames.html', context)

        elif request.method == 'POST':
            if 'uploaded_file' not in request.FILES:
                context['form_message'] = 'Please upload a file of usernames to be whitelisted.'
                return TemplateResponse(request, 'students/add_whitelisted_usernames.html', context)

            whitelist = request.FILES['uploaded_file']
            cleaned_names = [name.strip().lower() for name in whitelist.readlines()]

            for name in cleaned_names:
                temp = WhitelistedUsername(username=name)
                temp.save()

            context['form_message'] = 'Usernames successfully whitelisted!'
            return TemplateResponse(request, 'students/add_whitelisted_usernames.html', context)


# manage bookings via the admin interface
admin.site.register(Booking)


# manage Robot Terminals via the admin interface
admin.site.register(
    RobotTerminal,
    list_display=['id', 'title'],
    list_display_links=['id'],
)
