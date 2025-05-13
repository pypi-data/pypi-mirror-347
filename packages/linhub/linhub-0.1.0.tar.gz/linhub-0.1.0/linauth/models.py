from datetime import datetime
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.template import loader
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string


def avatar_directory_path(instance, filename):
    return 'avatar/{0}_{1}'.format(datetime.timestamp(datetime.now()), filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=avatar_directory_path,
        null=True,
        blank=True,
        height_field=None,
        width_field=None,
        max_length=None)


class CustomAnonymousUser(AnonymousUser):
    email = 'anonymous@linalgo.com'


@receiver(post_save, sender='linauth.User')
def on_new_user(sender, instance, created, signal, *args, **kwargs):
    if created:
        subject_template = 'email/new_user_notification_subject.txt'
        body_template = 'email/new_user_notification_body.html'

        from_email = settings.NEW_USER_NOTIFICATION_FROM_EMAIL
        to_emails = settings.NEW_USER_NOTIFICATION_TO_EMAILS
        context = {'user': instance}

        subject = render_to_string(subject_template, context).strip()
        message = render_to_string(body_template, context)

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=to_emails,
            html_message=message
        )
