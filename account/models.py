from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class User(AbstractBaseUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Номер',
        null=True,
        blank=True,
        unique=True
    )
    surname = models.CharField(
        verbose_name='Имя, Фамилия',
        max_length=100
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='персонал'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=False
    )
    reset_password_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        editable=False
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активен'
    )
    access = models.BooleanField(
        verbose_name='Доступ',
        default=False
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def str(self):
        return f"{self.email}" or f"{self.phone_number}"

