from django.core.mail import send_mail
from django.conf import settings

def send_email(symbol, is_master, source):
    if is_master:
        url = 'http://{}/world_of_coins'.format(settings.ALLOWED_HOSTS[0])
    else:
        url = 'http://{}/coins'.format(settings.ALLOWED_HOSTS[0])

    send_mail(
        'Qobit Notification',
        'New coin ( {} ) is discovered from {}. Go to {} and check it.'
        .format(symbol, source, url),
        settings.DEFAULT_FROM_EMAIL,
        ['alerts@qobit.com', 'ellis.zoric@qobit.com'],
        fail_silently=False,
    )
