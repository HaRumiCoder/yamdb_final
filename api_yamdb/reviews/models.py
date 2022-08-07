from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import ROLES


class User(AbstractUser):
    USERNAME_FIELDS = 'username'

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default='user',
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(max_length=64)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField()
    year = models.DateField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.text[:15]


class Review(Message):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_for_title'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(Message):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
