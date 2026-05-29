# MySite/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.conf.urls import handler404

# Импорт кастомного AdminSite (для продвинутого уровня ЛБ14)
from lex.admin_site import custom_admin_site

# Кастомная страница 404
handler404 = 'lex.views.custom_404'


def home(request):
    """Главная страница сайта"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lex</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            a {
                display: block;
                padding: 10px 15px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                max-width: 300px;
            }
            a:hover { background: #0056b3; }
            .app-section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать на сайт!</h1>

        <div class="app-section">
            <h2>📱 Приложения:</h2>
            <ul>
                <li><a href="/lex/">🏠 Приложение Lex</a></li>
                <li><a href="/lex-admin/">🎨 Кастомная админ-панель</a></li>
            </ul>
        </div>

        <div class="app-section">
            <h2>🔗 Страницы приложения Lex:</h2>
            <ul>
                <li><a href="/lex/">🏠 Главная Lex</a></li>
                <li><a href="/lex/test/">🧪 Тестовая страница</a></li>
                <li><a href="/lex/about/">ℹ️ О нас</a></li>
                <li><a href="/lex/news/">📰 Список новостей</a></li>
                <li><a href="/lex/news/add/">➕ Добавить новость</a></li>
            </ul>
        </div>
    </body>
    </html>
    """)


urlpatterns = [
    # Админ-панели
    path('admin/', admin.site.urls),
    path('lex-admin/', custom_admin_site.urls),

    # Приложение Lex
    path('lex/', include('lex.urls')),

    # Главная страница
    path('', home, name='home'),
]

# ============================================
# НАСТРОЙКА ДЛЯ РЕЖИМА ОТЛАДКИ (DEBUG = True)
# ============================================

if settings.DEBUG:
    # Django Debug Toolbar - ОТКЛЮЧЕН
    # (раскомментируйте если понадобится)
    # try:
    #     import debug_toolbar
    #     urlpatterns = [
    #         path('__debug__/', include(debug_toolbar.urls)),
    #     ] + urlpatterns
    # except ImportError:
    #     pass

    # Обслуживание медиа-файлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Обслуживание статических файлов
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)