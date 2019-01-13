import os

def run_celery_worker():
    os.system('celery -A rarestpupper.celeryapp worker -l info')

if __name__ == '__main__':
    run_celery_worker()
