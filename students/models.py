from __future__ import unicode_literals

from channels import Group
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import json
from pexpect import pxssh
from simplegist import Simplegist
from StringIO import StringIO


class WhitelistedUsername(models.Model):
    # TODO: change this username field to only allow usernames matching the UCT
    # student number regex
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(WhitelistedUsername, self).save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(User, editable=False, default=None, blank=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)

    def __str__(self):
        return "%s: %s - %s" % (self.user, self.start_time, self.end_time)


class RobotTerminal(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        # The group that channels need to subscribe to for messages
        return Group("robot-%s" % self.id)

    def send_command(self, command, user):
        lines = StringIO(command).readlines()

        initial_msg = {'robot': str(self.id), 'message': 'Connecting to robot...'}
        self.websocket_group.send(
            {"text": json.dumps(initial_msg)}
        )

        try:
            ssh = pxssh.pxssh()
            hostname = getattr(settings, 'ROBOT_HOSTNAME')
            username = getattr(settings, 'ROBOT_USERNAME')
            password = getattr(settings, 'ROBOT_PWD')
            ssh.login(hostname, username, password)

            ssh.sendline('cd HonoursProject')
            ssh.prompt()

            ssh.PROMPT = '>{3}|\.{3}'
            ssh.sendline('python')
            ssh.prompt()

            lines[-1] += '\n'
            lines = [l for l in lines if not l.startswith('#')]

            for line in lines:
                ssh.send(line)
                ssh.prompt()
                output_message = '... ' + ssh.before + '\n'
                fb = {'robot': str(self.id), 'message': output_message}
                self.websocket_group.send(
                    {"text": json.dumps(fb)}
                )

            ssh.PROMPT = '$'
            ssh.sendline('quit()')
            ssh.prompt()
            output_message = 'DONE\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {"text": json.dumps(fb)}
            )

            ssh.logout()
        except pxssh.ExceptionPxssh as e:
            output_message = "Could not connect to the robot."
            print(e)

        final_msg = {'robot': str(self.id), 'message': output_message}
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
