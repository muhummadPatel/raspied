from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Booking, RobotTerminal, WhitelistedUsername


@admin.register(WhitelistedUsername)
class WhitelistedUsernameAdmin(admin.ModelAdmin):
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
            # TODO: Use a form to validate this input
            if 'uploaded_file' not in request.FILES:
                context['form_message'] = 'Please upload a file of usernames to be whitelisted.'
                return TemplateResponse(request, 'students/add_whitelisted_usernames.html', context)

            whitelist = request.FILES['uploaded_file']
            cleaned_names = [name.strip().lower() for name in whitelist.readlines()]

            for name in cleaned_names:
                # NOTE: If this is slowing things down, look into bulk_create method
                temp = WhitelistedUsername(username=name)
                temp.save()

            context['form_message'] = 'Usernames successfully whitelisted!'
            return TemplateResponse(request, 'students/add_whitelisted_usernames.html', context)


admin.site.register(Booking)


admin.site.register(
    RobotTerminal,
    list_display=['id', 'title'],
    list_display_links=['id'],
)
