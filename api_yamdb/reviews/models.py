from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year_gt_current

User = get_user_model()


class Category(models.Model):
    """Категория (тип) произведения."""
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField('Произведение', max_length=256, db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год издания',
        validators=(validate_year_gt_current,),
        db_index=True,
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы с оценкой (1-10)."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка (1-10)',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        error_messages={
            'min_value': 'Оценка должна быть от 1 до 10!',
            'max_value': 'Оценка должна быть от 1 до 10!',
        }
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author',
            ),
        )
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """Комментарии к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:50]
