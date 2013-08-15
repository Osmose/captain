from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=256)
    homepage = models.URLField()

    class Meta:
        permissions = (
            ('can_run_commands', 'Can run commands'),
        )