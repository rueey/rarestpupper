import os

if __name__ == '__main__':
    os.system('celery -A rarestpupper.celeryapp beat -l info')
