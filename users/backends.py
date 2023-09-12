# This code defines a custom authentication backend that allows users to log in using their email address or username.

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates users based on their email address or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates the user.

        Args:
            request: The Django request object.
            username: The username or email address of the user.
            password: The password of the user.
            **kwargs: Keyword arguments.

        Returns:
            The authenticated user, if the credentials are valid.

        """
        try:
            # Get the user by username or email address.
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # The user does not exist.
            return None
        except UserModel.MultipleObjectsReturned:
            # Multiple users have the same username or email address.
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # Check the password.
        if user.check_password(password) and self.user_can_authenticate(user):
            # The credentials are valid. Return the user.
            return user

        # The credentials are invalid.
        return None

