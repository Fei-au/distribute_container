from django.core.management.base import BaseCommand
from pubsub.sub import receive_messages

class Command(BaseCommand):
    help = 'Runs the PubSub subscriber'

    def add_arguments(self, parser):
        parser.add_argument('--subscriber-id', type=str, required=True)
        parser.add_argument('--timeout', type=float, default=None)

    def handle(self, *args, **options):
        subscriber_id = options['subscriber_id']
        timeout = options['timeout']
        self.stdout.write(f'Starting subscriber {subscriber_id}')
        receive_messages(subscriber_id, timeout)
