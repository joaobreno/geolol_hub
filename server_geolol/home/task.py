from celery import shared_task
import time

@shared_task
def print_test():
    for _ in range(10):
        time.sleep(2)
        print('TO AQUI')