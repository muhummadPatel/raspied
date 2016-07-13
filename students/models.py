from __future__ import unicode_literals

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
