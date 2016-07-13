from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from registration import signals
from registration.backends.simple.views import RegistrationView

from .forms import ExclusiveRegistrationForm


User = get_user_model()


class ExclusiveRegistrationView(RegistrationView):
    form_class = ExclusiveRegistrationForm


@login_required
def home(request):
    context = {
        'streaming_server_ip': getattr(settings, 'STREAMING_SERVER_IP', '105.225.158.228')
    }
    return render(request, 'students/home.html', context)
