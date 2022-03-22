from django.core.mail import send_mail

def send(user_email, login, password):
    print('email sanded')
    send_mail(
        'Вы зарегестрировались на NFTGenerator',
        f'Вы сможете войти на сервис с этими данными: login: {login}, password: {password}',
        'zipnftgenerator@gmail.com',
        [user_email],
        fail_silently=False,
    )