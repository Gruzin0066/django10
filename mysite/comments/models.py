from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post  # предположим, что у вас есть приложение blog
# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Рейтинг',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'

    # def get_absolute_url(self):
    #     return reverse('post_detail', kwargs={'pk': self.post.pk})

    def get_absolute_url(self):
        # Используйте правильное имя URL из вашего приложения blog
        return reverse('post', kwargs={'slug': self.post.slug})  # ← исправлено на 'post'