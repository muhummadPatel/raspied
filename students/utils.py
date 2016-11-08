from datetime import datetime

from .exceptions import ClientError
from .models import Booking, RobotTerminal


def get_robot_terminal_or_error(robot_id, user):
    """
    Returns the robot terminal for the given robot_id if it exists and the user
    has the curent booking for it.
    """
    # Check if the user is logged in
    if not user.is_authenticated():
        raise ClientError('USER_HAS_TO_LOGIN')

    # get the robot_terminal with the given id
    try:
        robot = RobotTerminal.objects.get(pk=robot_id)
    except RobotTerminal.DoesNotExist:
        raise ClientError('ROBOT_INVALID')

    # Check permissions
    now = datetime.now()
    has_booking = len(Booking.objects.filter(user=user, start_time__lte=now, end_time__gte=now)) > 0
    if not (user.is_staff or has_booking):
        raise ClientError('ROBOT_ACCESS_DENIED')

    return robot


def get_booked_robot(user):
    """
    Returns the robot terminal of the robot that the given user currently has
    booked, otherwise returns None.
    """
    now = datetime.now()
    has_booking = len(Booking.objects.filter(user=user, start_time__lte=now, end_time__gte=now)) > 0

    if has_booking or user.is_staff:
        # TODO: To support multiple robots, we will need to pull in the robot_id from the booking
        return RobotTerminal.objects.first()
