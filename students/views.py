from django.contrib.auth import authenticate, get_user_model, login

from registration import signals
from registration.backends.simple.views import RegistrationView

from .forms import ExclusiveRegistrationForm


User = get_user_model()


class ExclusiveRegistrationView(RegistrationView):
    form_class = ExclusiveRegistrationForm
