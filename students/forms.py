from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm

from .models import WhitelistedUsername


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    """
    Extension of default AuthenticationForm to replace 'username' label with 'student number'.
    """
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Student number'


class ExclusiveRegistrationForm(RegistrationForm):
    """
    Extension of default RegistrationForm to replace 'username' label with
    'student number' and only allow registration with whitelisted usernames.
    """
    def __init__(self, *args, **kwargs):
        super(ExclusiveRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Student number'

    def clean(self):
        form_username = self.cleaned_data['username']
        try:
            # If this runs without raising an exception, then the username is in
            # our database of whitelisted usernames.
            WhitelistedUsername.objects.get(username=form_username.lower())
        except ObjectDoesNotExist:
            err = ValidationError(_('Unrecognised student number. Are you a CS1 student at UCT?s'), code='invalid')
            self.add_error(User.USERNAME_FIELD, err)

        super(ExclusiveRegistrationForm, self).clean()
