from linhub import backends, models


def invite_collaborator(email, role, organization, request=None):
    if email is not None:
        backend = backends.LinHubInvitationBackend()
        user = backend.invite_by_email(
            email=email,
            domain=request.get_host,
            organization=organization,
            sender=request.user)
    collaborator, _ = models.Collaborator.objects.get_or_create(
        user=user, organization=organization)
    collaborator.role = role
    collaborator.save()
    return collaborator
