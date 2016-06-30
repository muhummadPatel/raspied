from django.conf.urls import url

from . import views

app_name = "todo"
urlpatterns = [
    url(r'^$', views.index, name='students_index'),
]
