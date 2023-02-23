from django.contrib.auth.base_user import BaseUserManager
from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as error:
            print(f'Error while create new user: {error}')
            raise

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        return self._create_user(username, password, **extra_fields)

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = [('Admin', 'Администратор'), ('Client', 'Клиент'), ('Courier', 'Курьер')]

    username = models.CharField(
        verbose_name='Логин',
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    birthday = models.DateField(
        verbose_name='Дата рождения'
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=255,
        choices=USER_ROLES,
        default='Client'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username



# model with user address