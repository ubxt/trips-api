from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def create_passenger_email_task():
    logger.info("Sent passenger created email")
    return "Passenger created mail sent"
