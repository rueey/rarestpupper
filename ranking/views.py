from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from .models import Pupper
from .utils import check_task_finished, setup_database

# Create your views here.
def leaderboard(request):
    context_dict = {'top_scoring_pupper_list': Pupper.objects.order_by('-score')[:5]}
    return render(request, 'ranking/leaderboard.html', context_dict)

def get_puppers(request):
    if(request.method == 'GET'):
        try:
            order_by = request.GET.get('order_by', 'score')
            puppers = Pupper.objects.order_by('-' + order_by)[:5]
            ret = []
            for p in puppers:
                ret.append({'name': p.species, 'score': p.score, 'aggregate_score': p.aggregate_score, 'time': p.update_time})
            return JsonResponse({'data': ret}, status=200)
        except:
            return JsonResponse({'error': 'no puppers'}, status=400)
    else:
        return JsonResponse({'error': 'wrong method'}, status=400)
        