from django.contrib.auth.signals import user_logged_in
from users.models import BaseUser
from django.dispatch import receiver


@receiver(user_logged_in, sender=BaseUser)
def login_user(sender, request, user, **kwargs):
    BaseUser.login_count = BaseUser.login_count + 1
    BaseUser.save()


user_logged_in.connect(login_user, sender=BaseUser,)
