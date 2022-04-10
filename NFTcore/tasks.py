from NFTGenerator.celery import app
from .services import test


@app.task
def start_test():
    test()