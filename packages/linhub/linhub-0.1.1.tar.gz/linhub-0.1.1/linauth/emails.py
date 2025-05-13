from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.email import BaseEmailMessage


class PasswordResetEmail(BaseEmailMessage):
    template_name = 'email/password_reset.html'

    def get_context_data(self):
        context = super(PasswordResetEmail, self).get_context_data()

        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['site_name'] = settings.SITE_NAME
        context['domain'] = settings.SITE_DOMAIN
        context['protocol'] = settings.SITE_PROTOCOL
        context['url'] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
