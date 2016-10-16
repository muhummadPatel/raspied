from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomAuthenticationForm

app_name = 'students'
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^booking/$', views.booking, name='booking'),
    url(r'^booking/list/$', views.booking_list, name='list_booking'),
    url(r'^booking/listall/(?P<booking_date>\d{2}\.{1}[a-zA-Z]+\.{1}\d{4})/$', views.booking_listall,
        name='listall_booking'),
    url(r'^booking/(?P<booking_id>[\d]+)/delete/$', views.booking_delete, name='delete_booking'),
    # TODO: overidden registration urls come before the include below
    url(r'^accounts/login/$', views.custom_login, name='registration_login'),
    url(r'^accounts/register/$', views.ExclusiveRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
