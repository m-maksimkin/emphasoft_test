from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


User = get_user_model()


@receiver(user_signed_up)
def social_signup_email_verify(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        user.email_verified = True
        user.save()
