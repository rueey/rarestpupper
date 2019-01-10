from .models import Pupper
from django.utils import timezone

def save_dog_model(species, score):
    obj, created = Pupper.objects.get_or_create(species=species, score=score, update_time=timezone.now())
    if not created:
        obj.aggregate_score = obj.aggregate_score + score
        obj.save()
