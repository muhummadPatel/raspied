from django.conf.urls import include, url

from . import views

app_name = "students"
urlpatterns = [
    # TODO: overidden registration urls come before the include below
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
