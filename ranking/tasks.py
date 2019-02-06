from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import task

from . import query_reddit, utils, models, consts
from . import models

'''FINISHED = 0, RUNNING = 1'''
running_state = 0

logger = get_task_logger(__name__)

def task_finished():
    running_state = 0

def task_running():
    running_state = 1

'''Asynchronous periodic task for updating scores.'''

@task(name='ranking.tasks.update_scores')
def update_scores():
    logger.info("Updating scores")
    task_running()
    score_dict = query_reddit.get_scores_from_parsed_json(query_reddit.get_hottest_posts(query_reddit.get_auth_token()))
    if(len(models.Pupper.objects.all()) == 0):
        logger.info("Setting up database for the first time")
        utils.setup_database()
    for key, value in score_dict.items():
        utils.save_dog_model(key, value)
    logger.info("Updated scores and saved models")
    task_finished()

