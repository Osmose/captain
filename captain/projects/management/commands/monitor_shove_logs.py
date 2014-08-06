import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from captain.projects import shove
from captain.projects.models import CommandLog


log = logging.getLogger(__name__)


def handle_log_event(data):
    try:
        log_key = data['log_key']
        return_code = data['return_code']
        output = data['output']
    except KeyError:
        log.warning('Could not parse incoming log event: `{0}`.'.format(data))
        return

    try:
        command_log = CommandLog.objects.get(pk=log_key)
    except (CommandLog.DoesNotExist, ValueError):
        log.warning('Could not save log for log key `{0}`.'.format(log_key))
        return

    log.info('Writing log for {0}.'.format(command_log))
    command_log.return_code = return_code
    command_log.log = output
    command_log.save()


class Command(BaseCommand):
    help = 'Listen for log events from shove and write out logfiles for them.'

    def handle(self, *args, **kwargs):
        # Log INFO events to make the commandline output a little more useful.
        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
        shove.consume(settings.LOGGING_QUEUE, handle_log_event)
