# lex/urls.py
from django.urls import path
from . import views

app_name = 'lex'

urlpatterns = [
    # ============================================
    # ОСНОВНЫЕ МАРШРУТЫ (ПРЕДСТАВЛЕНИЯ НА ОСНОВЕ КЛАССОВ)
    # ============================================
    path('', views.HomeNews.as_view(), name='index'),
    path('test/', views.test, name='test'),
    path('about/', views.about, name='about'),

    # ============================================
    # МАРШРУТЫ ДЛЯ НОВОСТЕЙ
    # ============================================
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.ViewNews.as_view(), name='news_detail'),
    path('news/category/<int:category_id>/', views.NewsByCategory.as_view(), name='news_by_category'),

    # ============================================
    # РЕДАКТИРОВАНИЕ НОВОСТИ (ИЗ ЛАБОРАТОРНОЙ №11)
    # ============================================
    path('news/edit/<int:news_id>/', views.edit_news, name='edit_news'),

    # ============================================
    # ДОБАВЛЕНИЕ НОВОСТИ (CREATEVIEW - ЛАБОРАТОРНАЯ №12)
    # ============================================
    path('news/add/', views.CreateNews.as_view(), name='add_news'),

    # ============================================
    # МАРШРУТЫ ДЛЯ СУДЕБНЫХ ДЕЛ
    # ============================================
    path('cases/', views.case_list, name='case_list'),
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),
    path('practice-areas/', views.practice_areas_list, name='practice_areas_list'),
    path('cases/add/', views.add_case, name='add_case'),
    path('cases/<int:case_id>/edit/', views.edit_case, name='edit_case'),
    path('search/', views.search_cases, name='search_cases'),

    # ============================================
    # API МАРШРУТЫ
    # ============================================
    path('api/cases/', views.api_case_list, name='api_case_list'),
    path('api/cases/<int:case_id>/', views.api_case_detail, name='api_case_detail'),

    # ============================================
    # ТЕСТОВЫЕ МАРШРУТЫ
    # ============================================
    path('test/bootstrap/', views.test_bootstrap, name='test_bootstrap'),
    path('test/template-tags/', views.test_template_tags, name='test_template_tags'),

    # ============================================
    # РЕДИРЕКТЫ
    # ============================================
    path('go-to-category/<int:category_id>/', views.redirect_to_category, name='go_to_category'),
    path('go-to-news/<int:news_id>/', views.redirect_to_news, name='go_to_news'),
    path('go-home/', views.redirect_to_home, name='go_home'),
]