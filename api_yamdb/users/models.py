from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE = (
        (USER, 'User role'),
        (MODERATOR, 'Moderator role'),
        (ADMIN, 'Admin role'),
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='30 символом максимум. Символы только @/./+/-/_.',
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        help_text='Введите вашу почту',
    )
    bio = models.TextField(
        'Информация пользователе',
        blank=True,
        help_text='Описание пользователя',
    )
    confirmation_code = models.CharField('Код подтверждения', max_length=20)
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE,
        default='user',
        verbose_name='Роль пользователя',
        help_text='Выберите роль пользователя',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
