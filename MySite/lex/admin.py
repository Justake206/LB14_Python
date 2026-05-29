# lex/admin.py
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import PracticeArea, Case, News, Comment

# Пробуем импортировать кастомный AdminSite (если файл существует)
try:
    from .admin_site import custom_admin_site

    HAS_CUSTOM_ADMIN = True
except ImportError:
    HAS_CUSTOM_ADMIN = False


# ============================================
# БАЗОВЫЙ АДМИН-КЛАСС С ОГРАНИЧЕНИЯМИ
# ============================================

class BaseModelAdmin(ModelAdmin):
    """
    Базовый класс для всех админ-моделей
    """

    def get_actions(self, request):
        actions = super().get_actions(request)

        # Если пользователь не является суперпользователем
        if not request.user.is_superuser:
            # Удаляем действие массового удаления
            if 'delete_selected' in actions:
                del actions['delete_selected']

        return actions


# ============================================
# АДМИН-КЛАССЫ ДЛЯ МОДЕЛЕЙ
# ============================================

class PracticeAreaAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'slug', 'description_short')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    description_short.short_description = 'Описание'


class NewsAdmin(BaseModelAdmin):
    list_display = ('id', 'title_short', 'category', 'is_published', 'views', 'created_at_short')
    list_display_links = ('title_short',)
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_select_related = ('category',)
    readonly_fields = ('created_at', 'updated_at', 'views')

    # Включаем кнопку просмотра на сайте
    view_on_site = True

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'category', 'photo')
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
        ('Статистика', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )

    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title

    title_short.short_description = 'Заголовок'

    def created_at_short(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    created_at_short.short_description = 'Дата создания'

    # Кастомные действия
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} новостей опубликовано.')

    make_published.short_description = 'Опубликовать выбранные новости'

    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} новостей снято с публикации.')

    make_unpublished.short_description = 'Снять с публикации выбранные новости'


class CommentAdmin(BaseModelAdmin):
    list_display = ('id', 'news_short', 'author', 'rating', 'is_moderated', 'created_at_short')
    list_filter = ('is_moderated', 'rating', 'created_at')
    search_fields = ('author', 'text', 'email')
    list_editable = ('is_moderated',)
    readonly_fields = ('created_at',)

    def news_short(self, obj):
        return obj.news.title[:40] + '...' if len(obj.news.title) > 40 else obj.news.title

    news_short.short_description = 'Новость'

    def created_at_short(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    created_at_short.short_description = 'Дата'

    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_moderated=True)
        self.message_user(request, f'{updated} комментариев одобрено.')

    approve_comments.short_description = 'Одобрить выбранные комментарии'

    def reject_comments(self, request, queryset):
        updated = queryset.update(is_moderated=False)
        self.message_user(request, f'{updated} комментариев отклонено.')

    reject_comments.short_description = 'Отклонить выбранные комментарии'


class CaseAdmin(BaseModelAdmin):
    list_display = ('case_number', 'title_short', 'client', 'practice_area', 'status', 'created_at')
    list_filter = ('status', 'practice_area', 'is_confidential')
    search_fields = ('case_number', 'title', 'client')
    list_select_related = ('practice_area',)
    readonly_fields = ('created_at', 'updated_at')

    view_on_site = True

    def title_short(self, obj):
        return obj.title[:40] + '...' if len(obj.title) > 40 else obj.title

    title_short.short_description = 'Название'


# ============================================
# РЕГИСТРАЦИЯ В ОБЫЧНОЙ АДМИНКЕ
# ============================================

admin.site.register(PracticeArea, PracticeAreaAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)

# ============================================
# РЕГИСТРАЦИЯ В КАСТОМНОЙ АДМИНКЕ (если есть)
# ============================================

if HAS_CUSTOM_ADMIN:
    custom_admin_site.register(PracticeArea, PracticeAreaAdmin)
    custom_admin_site.register(Case, CaseAdmin)
    custom_admin_site.register(News, NewsAdmin)
    custom_admin_site.register(Comment, CommentAdmin)