from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    email_or_phone_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email_or_phone_number', 'surname', 'password')

    def validate_email_or_phone_number(self, value):
        if '@' in value:
            self.email = value.lower()
            self.phone_number = None
            if User.objects.filter(email=self.email).exists():
                raise ValidationError("Пользователь с такой электронной почтой уже зарегистрирован.")
        else:
            self.phone_number = value
            self.email = None
            if User.objects.filter(phone_number=self.phone_number).exists():
                raise ValidationError("Пользователь с таким номером телефона уже зарегистрирован.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=self.email,
            phone_number=self.phone_number,
            password=validated_data['password'],
            surname=validated_data['surname']
        )
        user.is_active = True
        user.save()
        return user
