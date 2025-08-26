from django.db import models
from django.urls import reverse


# Create your models here.
class PostTags(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Тег')
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    def __str__(self):
        return self.tag


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=100, unique=True, verbose_name='URL')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('cat', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Post(models.Model):
    class Status(models.IntegerChoices):
        published = 1, 'Опубликовано'
        draft = 0, 'Черновик'
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменён', null=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.draft)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(PostTags, related_name='tags', verbose_name='Теги', blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото", blank=True, null=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']

    def active_comments(self):
        """Возвращает только активные комментарии"""
        return self.comments.filter(is_active=True)

    def active_comments_count(self):
        """Возвращает количество активных комментариев"""
        return self.comments.filter(is_active=True).count()

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея изображений'