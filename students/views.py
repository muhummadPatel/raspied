from datetime import datetime, timedelta
from dateutil import parser as timestring_parser
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from registration import signals
from registration.backends.simple.views import RegistrationView

from .forms import ExclusiveRegistrationForm
from .models import Booking


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

@login_required
@require_http_methods(['GET', 'POST'])
def booking(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'students/booking.html', context)
    if request.method =='POST':
        try:
            parsed_timestring = timestring_parser.parse(request.POST['datetime_str'])
        except ValueError, OverflowError:
            #TODO: return a useful error message for use in the ajax failure callback
            return HttpResponse('', status=400)

        user = request.user
        start_time = parsed_timestring
        end_time = start_time + timedelta(minutes=getattr(settings, 'BOOKNG_INTERVAL', 60))

        try:
            new_booking = Booking(user=user, start_time=start_time, end_time=end_time)
            new_booking.save()

            return HttpResponse('', status=200)
        except AttributeError, ValueError:
            return HttpResponse('', status=400)
