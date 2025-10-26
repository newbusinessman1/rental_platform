# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from users.services import set_user_role

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[("host","host"), ("guest","guest")], default="guest")
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "guest")
        user = User.objects.create_user(**validated_data)
        set_user_role(user, role)  # синхронизируем профиль + группы
        return user
