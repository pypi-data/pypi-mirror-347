import requests

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template import loader
from django.urls import reverse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from djoser.serializers import UserCreateSerializer
from djoser.compat import get_user_email
from djoser import signals
from djoser.conf import settings as dj_settings

from . import models, serializers


def create_user_and_organization(username, first_name, last_name, email, password=None):
    user = get_user_model().objects.get(email=email)
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    if password is not None:
        user.set_password(password)
    user.save()
    organization, _ = models.Organization.objects.get_or_create(
        name=username, email=email, individual=True, person=user)
    organization.save()
    collaborator = models.Collaborator(
        user=user, organization=organization, role=models.Collaborator.OWNER)
    collaborator.save()
    annotator, created = models.Annotator.objects.get_or_create(
        owner=user, model=models.Annotator.HUMAN)
    annotator.name = username
    annotator.save()
    return user


class RegistrationView(generics.GenericAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():

            user_s = UserCreateSerializer(data=serializer.data)

            try:
                user_s.is_valid(raise_exception=True)

                user = user_s.save()
                signals.user_registered.send(
                    sender=self.__class__, user=user, request=self.request
                )

                context = {'user': user}
                to = [get_user_email(user)]
                if dj_settings.SEND_ACTIVATION_EMAIL:
                    dj_settings.EMAIL.activation(self.request, context)\
                        .send(to)
                elif dj_settings.SEND_CONFIRMATION_EMAIL:
                    dj_settings.EMAIL.confirmation(self.request, context)\
                        .send(to)
                
                user = create_user_and_organization(
                    username=serializer.validated_data['username'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'])
                self.email_message(user)
                return Response(serializer.data, 
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(user_s.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def email_message(self, user):

        subject_template = 'email/welcome_subject.txt'
        body_template = 'email/welcome_body.html'

        from_email = 'Linalgo <registration@linalgo.com>'
        reply_to = ['Linalgo <support@linalgo.com>']
        context = {'user': user, 'domain': 'https://linhub.net'}

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(context).strip()
        body = body_template.render(context)
        msg = EmailMessage(
            subject, body, from_email, [user.email], reply_to=reply_to)
        msg.send(fail_silently=False)


class ActivationView(generics.GenericAPIView):
    serializer_class = serializers.UserActivationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = serializers.UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            url = 'http://' + request.get_host() + '/auth/users/activate'
            response = requests.post(url, data=serializer.data)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                user = create_user_and_organization(
                    username=serializer.validated_data['username'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'])
                self.email_message(user)
                return Response(serializer.data, status=response.status_code)
            else:
                return Response(response.json(), response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def email_message(self, user):

        subject_template = 'email/welcome_subject.txt'
        body_template = 'email/welcome_body.html'

        from_email = 'Linalgo <registration@linalgo.com>'
        reply_to = ['Linalgo <support@linalgo.com>']
        context = {'user': user, 'domain': 'https://linhub.net'}

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(context).strip()
        body = body_template.render(context)
        msg = EmailMessage(
            subject, body, from_email, [user.email], reply_to=reply_to)
        msg.send(fail_silently=False)


class AskInvitationView(generics.GenericAPIView):
    serializer_class = serializers.AskInvitationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = serializers.AskInvitationSerializer(data=request.data)
        if serializer.is_valid():
            user = {
                'username': serializer.validated_data['name'],
                'email': serializer.validated_data['email'],
                'company': serializer.validated_data['company'],
                'role': serializer.validated_data['role']
            }
            self.email_message(user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def email_message(self, user):

        subject_template = 'email/ask4invite_subject.txt'
        body_template = 'email/ask4invite_body.html'

        from_email = 'Linalgo <invite@linalgo.com>'
        reply_to = ['Linalgo <invite@linalgo.com>']
        to_emails = [user['email'], from_email]
        context = {'user': user, 'domain': 'https://linhub.net'}

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(context).strip()
        body = body_template.render(context)
        msg = EmailMessage(
            subject, body, from_email, to_emails, reply_to=reply_to)
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
