from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from .models import Profile

User = get_user_model()


class BaseUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = BaseUserInfoSerializer(required=False)
    membership = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ["user", "date_of_birth", "membership"]

    def update(self, instance, validated_data):
        with transaction.atomic():
            base_user_info = validated_data.pop("user", None)
            if base_user_info:
                user = instance.user
                for attr, value in base_user_info.items():
                    setattr(user, attr, value)
                user.save()
            return super().update(instance, validated_data)
