from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Profile(models.Model):
    MEMBERSHIP_STATUS = [("regular", "Regular"), ("premium", "Premium")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(null=True)
    membership = models.CharField(
        max_length=10, choices=MEMBERSHIP_STATUS, default="regular"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
