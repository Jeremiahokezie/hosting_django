from django.conf import settings
from django.core.mail import EmailMessage

email = EmailMessage(
    'Test Email',
    'Hi there it worked',
    settings.EMAIL_HOST_USER,
    ['okeziejeremiahemenike@gmail.com']
)

email.fail_silently = True
email.send()
print('Email sent')