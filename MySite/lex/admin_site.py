# lex/admin_site.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class CustomAdminSite(AdminSite):
    """
    Кастомный AdminSite с изменённым заголовком и шаблоном
    Для лабораторной работы №14 (продвинутый уровень)
    """
    # Заголовок сайта (вкладка браузера)
    site_title = _('Lex - Панель управления')

    # Заголовок на странице входа
    site_header = _('Юридическая фирма "Lex"')

    # Индексный заголовок
    index_title = _('Добро пожаловать в панель управления Lex')


# Создаём экземпляр кастомного админ-сайта
custom_admin_site = CustomAdminSite(name='lex_admin') #111