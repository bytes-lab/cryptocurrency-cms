from django.core.mail import send_mail

def send_email(symbol, is_master, source):
    if is_master:
        url = 'http://localhost:8000/world_of_coins'
    else:
        url = 'http://localhost:8000/coins'

    send_mail(
        'Qobit Notification',
        'New coin ( {} ) is discovered from {}. Go to {} and check it.'
        .format(symbol, source, url),
        'info@qobit.com',
        ['jason.5001001@gmail.com'],
        fail_silently=False,
    )
