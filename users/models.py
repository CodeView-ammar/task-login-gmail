from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# This is a custom user model that extends the AbstractUser model.
# It adds three new fields: is_super_admin, is_stuff, and is_customer.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_super_admin=models.BooleanField(default=False)
    is_stuff=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)

    # This method overrides the create_superuser() method from the AbstractUser model.
    # It ensures that the superuser has the is_admin, is_staff, and is_superuser fields set to True.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must be Admin")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be staff")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self.create_user(email, password, **extra_fields)

    # This method overrides the save() method from the AbstractUser model.
    # It ensures that the is_customer field is set to True for all users, except for superusers.
    def save(self, *args, **kwargs):
        
        if not self.is_super_admin:
            self.is_customer=True
        
        super().save(*args, **kwargs)

# This method ensures that the email field is unique.
CustomUser._meta.get_field('email')._unique = True


# This is a model that stores the profile information for each user.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    # This receiver is triggered whenever a new CustomUser is created.
    # It creates a new Profile object for the user.
    @receiver(post_save, sender=CustomUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
