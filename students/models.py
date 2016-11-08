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
    """
    Whitelisted usernames are the usernames/student numbers that have been
    authorised to register on the RASPIED site. Any registration attempt with a
    non WhitelistedUsername will fail.
    """
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(WhitelistedUsername, self).save(*args, **kwargs)


class Booking(models.Model):
    """
    These are the robot bookings. Helps keep track of which student
    is using the robot at any given time and manage shared access to the robot
    without any conflicts, etc.
    """
    user = models.ForeignKey(User, editable=False, default=None, blank=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)

    def __str__(self):
        return '%s: %s - %s' % (self.user, self.start_time, self.end_time)


class RobotTerminal(models.Model):
    """
    Models the connection with the robot. Also handles sending and running code,
    and halting code executions.
    """
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        # The group that channels need to subscribe to for messages
        return Group('robot-%s' % self.id)

    def get_indent(self, s):
        for i in range(len(s)):
            if s[i] != " ":
                return i

        return 0

    def sanitize_code_lines(self, lines):
        """
        Used to clean up the submitted code and format it to allow running it in
        the python shell. Makes sure the indents are handled properly.
        """
        out = []
        for i in range(len(lines)):
            next_line = ''
            if i+1 < len(lines):
                next_line = lines[i+1]

            if lines[i].startswith('#'):
                pass
            elif lines[i].strip():
                out.append(lines[i])

            if self.get_indent(next_line) == 0 and self.get_indent(next_line) < self.get_indent(lines[i]):
                # we have left an indented block, so send a newline
                out.append('\n')

        return out

    def send_halt(self):
        """
        Halts any currently executing Python processes on the Robot and recovers
        and resets the robot to its original state.
        """
        try:
            output_message = 'Attempting to kill the code...\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )
            ssh = pxssh.pxssh()
            hostname = getattr(settings, 'ROBOT_HOSTNAME')
            username = getattr(settings, 'ROBOT_USERNAME')
            password = getattr(settings, 'ROBOT_PWD')
            ssh.login(hostname, username, password)

            ssh.sendline("kill `ps -ef | awk '/[p]ython/{print $2}'`")
            ssh.prompt()

            ssh.sendline("cd HonoursProject")
            ssh.prompt()

            ssh.sendline("python recover.py")
            ssh.prompt()

            output_message = 'Code Halted\nDONE\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )

            ssh.logout()
        except pxssh.ExceptionPxssh as e:
            output_message = 'Could not connect to the robot.\nDONE\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )
            print(e)

    def send_command(self, command, user):
        """
        Sends the submitted script(command) to the robot and runs it one line at
        a time.
        """
        # split the code into lines and sanitize the lines
        lines = StringIO(command).readlines()
        lines[-1] += '\n'
        lines += ['\n\n\n']
        lines = self.sanitize_code_lines(lines)

        cleanup_lines = getattr(settings, 'CLEANUP_CODE')

        initial_msg = {'robot': str(self.id), 'message': 'Connecting to robot...\n'}
        self.websocket_group.send(
            {'text': json.dumps(initial_msg)}
        )

        try:
            # open ssh session to the robot
            ssh = pxssh.pxssh()
            hostname = getattr(settings, 'ROBOT_HOSTNAME')
            username = getattr(settings, 'ROBOT_USERNAME')
            password = getattr(settings, 'ROBOT_PWD')
            ssh.login(hostname, username, password)

            ssh.sendline('cd HonoursProject')
            ssh.prompt()

            # from now on, listen for the python prompt
            ssh.PROMPT = '>{3}|\.{3}'
            ssh.sendline('python')
            ssh.prompt()

            # send each line to the robot and report output to the client
            for line in lines:
                ssh.send(line)
                ssh.prompt()
                output_message = '... ' + ssh.before + '\n'
                fb = {'robot': str(self.id), 'message': output_message}
                self.websocket_group.send(
                    {'text': json.dumps(fb)}
                )

            output_message = 'Code execution complete. Now resetting the robot...'
            fb = {'robot': str(self.id), 'message': output_message, 'code_done': True}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )

            # send cleanup lines to reset the robot to its starting position
            for line in cleanup_lines:
                ssh.send(line)
                ssh.prompt()

            #  exit python shell and close ssh connection
            ssh.PROMPT = '$'
            ssh.sendline('quit()')
            ssh.prompt()
            output_message = 'DONE\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )

            ssh.logout()
        except pxssh.ExceptionPxssh as e:
            output_message = 'Could not connect to the robot.\nDONE\n'
            fb = {'robot': str(self.id), 'message': output_message}
            self.websocket_group.send(
                {'text': json.dumps(fb)}
            )
            print(e)

        final_msg = {'robot': str(self.id), 'message': output_message}
        self.websocket_group.send(
            {'text': json.dumps(final_msg)}
        )
