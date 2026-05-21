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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Метод обратного разрешения URL для категории.
        Возвращает URL на страницу новостей этой категории.
        """
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
        """Возвращает краткую информацию о деле"""
        return f"Дело №{self.case_number} - {self.client}"

    def get_status_color(self):
        """Возвращает цвет статуса для Bootstrap"""
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

    # Поле для изображения
    photo = models.ImageField(
        upload_to='news_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение новости'
    )

    # Связь с PracticeArea (категория новости)
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
        """
        Метод обратного разрешения URL для новости.
        Возвращает URL на детальную страницу новости.
        ВАЖНО: используем 'pk', так как в urls.py используется <int:pk>
        """
        return reverse('lex:news_detail', kwargs={'pk': self.pk})

    # Методы для использования в шаблонах
    def get_short_title(self):
        """Метод для получения сокращенного заголовка (первые 30 символов)"""
        if len(self.title) > 30:
            return self.title[:27] + '...'
        return self.title

    def get_news_type(self):
        """Метод для определения типа новости по категории"""
        if self.category:
            return f"Категория: {self.category.name}"
        return "Общие новости"

    def has_photo(self):
        """Проверяет, есть ли у новости изображение"""
        return bool(self.photo)

    def get_content_preview(self, words=50):
        """Возвращает превью контента (первые words слов)"""
        words_list = self.content.split()
        if len(words_list) > words:
            return ' '.join(words_list[:words]) + '...'
        return self.content

    def days_since_publication(self):
        """Возвращает количество дней с момента публикации"""
        from django.utils import timezone
        delta = timezone.now() - self.created_at
        return delta.days

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']