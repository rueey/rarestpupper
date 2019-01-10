from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import task

from . import query_reddit, utils

logger = get_task_logger(__name__)

@task()
def update_scores():
    logger.info("Updating scores")
    score_dict = query_reddit.get_scores_from_parsed_json(query_reddit.get_hottest_posts(query_reddit.get_auth_token()))
    for key, value in store_dict.items():
        utils.save_dog_model(key, value)
    logger.info("Updated scores and saved models")

