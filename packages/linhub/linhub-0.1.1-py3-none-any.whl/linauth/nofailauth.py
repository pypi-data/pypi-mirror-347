from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import AnonymousUser


class NoFailJWTAuthentication(JSONWebTokenAuthentication):
    """
    A jwt authentication method that doesn't fail
    """

    def authenticate(self, *args, **kwargs):
        try:
            return super(NoFailJWTAuthentication, self).authenticate(*args, **kwargs)
        except:
            return (AnonymousUser(), None)
