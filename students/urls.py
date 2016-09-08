from django.conf.urls import include, url

from . import views

app_name = "students"
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^booking/$', views.booking, name='booking'),
    # TODO: overidden registration urls come before the include below
    url(r'^accounts/register/$', views.ExclusiveRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
