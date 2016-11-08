from datetime import datetime, timedelta
from dateutil import parser as timestring_parser
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as default_login_view
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from registration import signals
from registration.backends.simple.views import RegistrationView

from .forms import CustomAuthenticationForm, ExclusiveRegistrationForm
from .models import Booking, RobotTerminal
from .utils import get_booked_robot


User = get_user_model()


class ExclusiveRegistrationView(RegistrationView):
    """
    Extended RegistrationView to use the custom ExclusiveRegistrationForm and
    set the success redirect to the home page rather than the index page.
    """
    form_class = ExclusiveRegistrationForm

    def get_success_url(self, user):
        self.request.session['is_first_login'] = True
        return 'students:home'


def custom_login(request):
    """
    Custom login view to use the CustomAuthenticationForm rather that the default.
    """
    return default_login_view(request, authentication_form=CustomAuthenticationForm)


@login_required
@require_http_methods(['GET'])
def home(request):
    """
    Render and return the home page. Send the video streaming server address as
    part of the context. Also, tell the template whether or not this is the user's
    first time logging in (so it knows whether to automatically start the tour).
    """
    context = {}
    context['streaming_server_ip'] = getattr(settings, 'STREAMING_SERVER_IP')

    if 'is_first_login' in request.session:
        context['is_first_login'] = request.session['is_first_login']
        del request.session['is_first_login']

    robot = get_booked_robot(request.user)
    if robot:
        context['robot'] = robot

    return render(request, 'students/home.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def booking(request):
    """
    Render and return the booking form. Also handle booking requests (POST) with
    all associated validations.
    """
    context = {}
    if request.method == 'GET':
        return render(request, 'students/booking.html', context)
    if request.method == 'POST':
        # figure out what date and time the user is trying to book
        try:
            timestring = request.POST['datetime_str']
            parsed_timestring = timestring_parser.parse(timestring)
        except (ValueError, OverflowError) as e:
            return HttpResponse('Unable to parse date', status=400)

        # figure out the start and end time of the requested booking
        user = request.user
        start_time = parsed_timestring
        end_time = start_time + timedelta(seconds=getattr(settings, 'BOOKING_INTERVAL', 3600) - 1)

        try:
            new_booking = Booking(user=user, start_time=start_time, end_time=end_time)

            # Checking for overlap/clashes
            day_bookings = Booking.objects.filter(
                            start_time__year=start_time.year,
                            start_time__month=start_time.month,
                            start_time__day=start_time.day)

            for booking in day_bookings:
                if (new_booking.start_time <= booking.end_time) and (new_booking.end_time >= booking.start_time):
                    return HttpResponse('Booking already taken', status=400)

            # Checking for too many bookings in this month (number of bookings must not exceed the defined quota)
            today = datetime.now()
            num_user_bookings = Booking.objects.filter(user=user, start_time__month=today.month).count()
            allowed_bookings_pm = getattr(settings, 'USER_BOOKINGS_PER_MONTH', 5)
            print
            if num_user_bookings + 1 > allowed_bookings_pm:
                return HttpResponse('Monthly booking quota exceeded', status=400)

            new_booking.save()

            return HttpResponse('Booking added', status=200)
        except (AttributeError, ValueError) as e:
            return HttpResponse('Could not save booking', status=400)


@login_required
@require_http_methods(['GET'])
def booking_list(request):
    """
    Return all future bookings owned by the requesting user.
    """
    today = datetime.now()
    today = today.replace(minute=0, second=0, microsecond=0)

    # get all the user bookings from this hour onwards
    user_bookings = Booking.objects.filter(user=request.user, start_time__gte=today).order_by('start_time')

    response_data = serializers.serialize('json', user_bookings)
    return HttpResponse(response_data, content_type='application/json')


@login_required
@require_http_methods(['GET'])
def booking_listall(request, booking_date):
    """
    Return all the bookings for the given booking_date (used to disable times in
    the booking form on the client side)
    """
    booking_date = timestring_parser.parse(booking_date)

    bookings = Booking.objects.filter(
                start_time__year=booking_date.year,
                start_time__month=booking_date.month,
                start_time__day=booking_date.day)

    response_data = serializers.serialize('json', bookings)
    return HttpResponse(response_data, content_type='application/json')


@login_required
@require_http_methods(['POST'])
def booking_delete(request, booking_id):
    """
    Delete the booking with the specified booking_id. Will only work if
    the booking is owned by the requesting user (You cannot delete someone elses
    bookings).
    """

    # get the booking to be deleted and make sure that it exists, is owned by the requesting user, and is in the future
    curr_time = datetime.now()
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user, start_time__gte=curr_time)
    booking.delete()

    return HttpResponse('Booking deleted', status=200)
