import os


def create_environment_variable():
    import logging
    from dotenv import load_dotenv

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('loading variable "SECRET_KEY" from .env')
    load_dotenv()
    if 'SECRET_KEY' not in os.environ:
        logger.info(".env don't have variable 'SECRET_KEY'")