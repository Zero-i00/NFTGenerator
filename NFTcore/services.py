from celery import Celery

from django.core.mail import send_mail
# from NFTGenerator.celery import app

app = Celery('tasks', broker='amqp://cqjouzla:ZXdWkGjatNhWVZC-KbAXvCeeOMdiHTHp@jaguar.rmq.cloudamqp.com/cqjouzla', backend='db+sqlite:///db.sqlite3')



def send(user_email, login, password):
    print('email sanded')
    send_mail(
        'Вы зарегестрировались на NFTGenerator',
        f'Вы сможете войти на сервис с этими данными: login: {login}, password: {password}',
        'zipnftgenerator@gmail.com',
        [user_email],
        fail_silently=False,
    )

@app.task
def test():
    print('hello')

