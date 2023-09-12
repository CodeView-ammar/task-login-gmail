# This code defines a custom token generator that is used to generate activation tokens.

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generate token based on user id, timestamp and is_active.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generate token hash value.

        Args:
            user: The user instance.
            timestamp: The timestamp.

        Returns:
            The token hash value.

        """
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
