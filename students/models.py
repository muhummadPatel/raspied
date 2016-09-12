from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


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
