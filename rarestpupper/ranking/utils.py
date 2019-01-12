from .models import Pupper
from django.utils import timezone
from celery import task
from celery import current_app
import pandas as pd
import ranking.consts as c

def setup_database():
    breeds = pd.read_csv('ranking/dog_breeds_classification/data/breeds.csv')
    list_of_breeds = breeds['breed'].values.tolist()
    for breed in list_of_breeds:
        Pupper(species=breed, update_time=timezone.now()).save()

def save_dog_model(species, score):
    obj, created = Pupper.objects.get_or_create(species=species, defaults={'score': score, 'update_time': timezone.now()})
    if not created:
        obj.score = score
        obj.aggregate_score = obj.aggregate_score + score
        obj.save()

def check_task_finished():
    current_app.loader.import_default_modules()
    update_task = current_app.tasks['tasks.update_scores']
    print(update_task)
    return update_task.AsyncResult(update_task.request.id).state
