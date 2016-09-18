import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from .models import RobotTerminal
from .utils import get_robot_terminal_or_error
from .exceptions import ClientError


# TODO: Add login required to all of these consumer methods?


@channel_session_user_from_http
def ws_connect(message):
    message.channel_session['robot'] = []


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel('robot.receive').send(payload)


@channel_session_user
def ws_disconnect(message):
    for robot_id in message.channel_session.get('robot', set()):
        try:
            robot = RobotTerminal.objects.get(pk=robot_id)
            robot.websocket_group.discard(message.reply_channel)
        except RobotTerminal.DoesNotExist:
            pass


@channel_session_user
def robot_terminal_join(message):
    try:
        robot = get_robot_terminal_or_error(message['robot'], message.user)

        # add user to the robot_terminal channel so that they get all the messages
        robot.websocket_group.add(message.reply_channel)
        message.channel_session['robot'] = list(set(message.channel_session['robot']).union([robot.id]))

        # send a join message to the channel so the client knows that they successfully joined
        message.reply_channel.send({
            'text': json.dumps({
                'join': str(robot.id),
                'title': robot.title,
            }),
        })
    except ClientError as e:
        e.send_to(message.reply_channel)


@channel_session_user
def robot_terminal_leave(message):
    try:
        # Reverse of join - remove them from everything.
        robot = get_robot_terminal_or_error(message['robot'], message.user)

        robot.websocket_group.discard(message.reply_channel)
        message.channel_session['robot'] = list(set(message.channel_session['robot']).difference([robot.id]))

        # send a leave message so the client knows that they have left the robot terminal
        message.reply_channel.send({
            'text': json.dumps({
                'leave': str(robot.id),
            }),
        })
    except ClientError as e:
        e.send_to(message.reply_channel)


@channel_session_user
def robot_terminal_send(message):
    try:
        # the user must be have joined the robot terminal in order to send a message
        if int(message['robot']) not in message.channel_session['robot']:
            raise ClientError('ROBOT_ACCESS_DENIED')

        # get the requested robot terminal and send the message (validations happen here)
        robot = get_robot_terminal_or_error(message['robot'], message.user)
        robot.send_command(message['message'], message.user)
    except ClientError as e:
        e.send_to(message.reply_channel)
