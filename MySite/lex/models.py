# lex/models.py
from django.db import models
from django.urls import reverse


# Create your models here.

class PracticeArea(models.Model):
    """
    Модель для областей юридической практики (категории новостей)
    """
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название области практики'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание области практики'
    )
    # Поле slug для задания 2
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name='URL-метка (slug)'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lex:news_by_category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Область практики'
        verbose_name_plural = 'Области практики'
        ordering = ['name']


class Case(models.Model):
    """
    Модель для судебных дел/кейсов
    """
    title = models.CharField(max_length=200, verbose_name='Название дела')
    case_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер дела'
    )
    client = models.CharField(max_length=200, verbose_name='Клиент')
    content = models.TextField(verbose_name='Описание дела')

    STATUS_CHOICES = [
        ('active', 'Активное'),
        ('closed', 'Закрыто'),
        ('pending', 'На рассмотрении'),
        ('appeal', 'Апелляция'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус дела'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата принятия дела'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    court_documents = models.FileField(
        upload_to='court_docs/%Y/%m/%d/',
        blank=True,
        verbose_name='Судебные документы'
    )

    is_confidential = models.BooleanField(
        default=False,
        verbose_name='Конфиденциальное дело'
    )

    practice_area = models.ForeignKey(
        PracticeArea,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Область практики'
    )

    def __str__(self):
        return f"{self.case_number}: {self.title}"

    def get_case_info(self):
        return f"Дело №{self.case_number} - {self.client}"

    def get_status_color(self):
        colors = {
            'active': 'success',
            'closed': 'secondary',
            'pending': 'warning',
            'appeal': 'info',
        }
        return colors.get(self.status, 'secondary')

    class Meta:
        verbose_name = 'Судебное дело'
        verbose_name_plural = 'Судебные дела'
        ordering = ['-created_at']


class News(models.Model):
    """
    Модель для новостей юридической фирмы
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок новости')
    content = models.TextField(verbose_name='Содержание новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    # Поле для количества просмотров (ЛБ13)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    photo = models.ImageField(
        upload_to='news_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение новости'
    )

    category = models.ForeignKey(
        PracticeArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория новости'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lex:news_detail', kwargs={'pk': self.pk})

    def get_short_title(self):
        if len(self.title) > 30:
            return self.title[:27] + '...'
        return self.title

    def get_news_type(self):
        if self.category:
            return f"Категория: {self.category.name}"
        return "Общие новости"

    def has_photo(self):
        return bool(self.photo)

    def get_content_preview(self, words=50):
        words_list = self.content.split()
        if len(words_list) > words:
            return ' '.join(words_list[:words]) + '...'
        return self.content

    def days_since_publication(self):
        from django.utils import timezone
        delta = timezone.now() - self.created_at
        return delta.days

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Модель для комментариев к новостям (ЛБ13)
    """
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Новость'
    )
    author = models.CharField(
        max_length=100,
        verbose_name='Автор комментария'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email автора'
    )
    text = models.TextField(verbose_name='Текст комментария')
    rating = models.IntegerField(
        default=0,
        verbose_name='Рейтинг комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_moderated = models.BooleanField(
        default=True,
        verbose_name='Промодерировано'
    )

    def __str__(self):
        return f"Комментарий от {self.author}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']