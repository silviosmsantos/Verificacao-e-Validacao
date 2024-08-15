from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def run_seed(sender, **kwargs):
    if sender.name == 'core':
        logger.info("Running seed_db command...")
        call_command('seed_db')
