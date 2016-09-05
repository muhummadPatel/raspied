from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from registration import signals
from registration.backends.simple.views import RegistrationView

from .forms import ExclusiveRegistrationForm


User = get_user_model()


class ExclusiveRegistrationView(RegistrationView):
    form_class = ExclusiveRegistrationForm


@login_required
@require_http_methods(['GET', 'POST'])
def home(request):
    context = {}
    if request.method == 'GET':
        print 'get view method'
        context['streaming_server_ip'] = getattr(settings, 'STREAMING_SERVER_IP', '105.225.158.228')
        return render(request, 'students/home.html', context)

    elif request.method == 'POST':
        print "post view method"
        if 'uploaded_file' not in request.FILES:
            context['user_script'] = "Could not upload file"
            return render(request, 'students/home.html', context)

        contents = request.FILES['uploaded_file'].read()
        print contents
        context['user_script'] = contents

        return render(request, 'students/home.html', context)
