# lex/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Case, PracticeArea, News
from .forms import NewsForm
from .mixins import PaginationMixin  # Миксин для пагинации (ЛБ14)


# ============================================
# ПРЕДСТАВЛЕНИЯ НА ОСНОВЕ КЛАССОВ (CBV)
# ============================================

class HomeNews(PaginationMixin, ListView):
    """
    Главная страница - список последних новостей.
    Заменяет функцию index().
    Оптимизировано с select_related (ЛБ14).
    Добавлена пагинация (ЛБ14).
    """
    model = News
    template_name = 'lex/index.html'
    context_object_name = 'latest_news'
    paginate_by = 8  # 8 новостей на страницу (ЛБ14)

    def get_queryset(self):
        """Возвращает только опубликованные новости с подгрузкой категории"""
        return News.objects.filter(
            is_published=True
        ).select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Добавляет статистику в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница - Lex'
        context['cases_count'] = Case.objects.count()
        context['practice_areas_count'] = PracticeArea.objects.count()
        context['news_count'] = News.objects.filter(is_published=True).count()
        return context


class ViewNews(DetailView):
    """
    Детальная страница новости.
    Заменяет функцию news_detail().
    Оптимизировано с select_related и prefetch_related (ЛБ14).
    """
    model = News
    template_name = 'lex/news_detail.html'
    context_object_name = 'news_item'

    def get_object(self, queryset=None):
        """
        Получает новость с подгрузкой категории и комментариев.
        Оптимизация SQL-запросов (ЛБ14).
        """
        return News.objects.select_related('category').prefetch_related('comments').get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Добавляет заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class NewsByCategory(PaginationMixin, ListView):
    """
    Список новостей по категории.
    Заменяет функцию news_by_category().
    Оптимизировано с select_related (ЛБ14).
    Добавлена пагинация (ЛБ14).
    """
    model = News
    template_name = 'lex/category_news.html'
    context_object_name = 'news_list'
    paginate_by = 6  # 6 новостей на страницу
    allow_empty = True

    def get_queryset(self):
        """Фильтрует новости по категории и статусу публикации"""
        self.category = get_object_or_404(PracticeArea, id=self.kwargs['category_id'])
        return News.objects.filter(
            category=self.category,
            is_published=True
        ).select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Добавляет данные о категории в контекст"""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Новости: {self.category.name}'
        context['news_count'] = self.get_queryset().count()
        context['active_category'] = self.category.id
        return context


class CreateNews(CreateView):
    """
    Форма добавления новости.
    ВАРИАНТ 14 (ЛБ11-12): проверка уникальности заголовка.
    """
    form_class = NewsForm
    template_name = 'lex/add_news.html'
    success_url = reverse_lazy('lex:index')

    def form_valid(self, form):
        """
        Проверяет, существует ли новость с таким заголовком.
        Если существует - добавляет ошибку валидации.
        """
        title = form.cleaned_data.get('title')

        # Проверка уникальности заголовка
        if News.objects.filter(title=title).exists():
            form.add_error('title', 'Новость с таким заголовком уже существует!')
            return self.form_invalid(form)

        return super().form_valid(form)


# ============================================
# ФУНКЦИИ ДЛЯ НОВОСТЕЙ (СПИСОК ВСЕХ НОВОСТЕЙ)
# ============================================

def news_list(request):
    """
    Список всех новостей с пагинацией.
    """
    # Получаем только опубликованные новости
    news_items = News.objects.filter(is_published=True).select_related('category').order_by('-created_at')

    # Пагинация - 6 новостей на страницу
    paginator = Paginator(news_items, 6)
    page = request.GET.get('page')

    try:
        news_page = paginator.page(page)
    except:
        news_page = paginator.page(1)

    context = {
        'news_list': news_page,
        'news_count': news_items.count(),
        'title': 'Новости юридической фирмы "Lex"',
        'paginator': paginator,
    }
    return render(request, 'lex/news_list.html', context)


# ============================================
# РЕДАКТИРОВАНИЕ НОВОСТИ (ИЗ ЛАБОРАТОРНОЙ №11)
# ============================================

def edit_news(request, news_id):
    """
    Редактирование существующей новости.
    Использует ModelForm для работы с моделью News.
    """
    news_item = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('lex:news_detail', pk=news_item.id)
    else:
        form = NewsForm(instance=news_item)

    context = {
        'form': form,
        'news_item': news_item,
        'title': f'Редактирование: {news_item.title}',
    }
    return render(request, 'lex/edit_news.html', context)


# ============================================
# ФУНКЦИИ ДЛЯ СТРАНИЦ
# ============================================

def about(request):
    """Страница "О нас" """
    context = {
        'title': 'О нас - Юридическая фирма "Lex"',
    }
    return render(request, 'lex/about.html', context)


def test(request):
    """Тестовая страница"""
    context = {
        'title': 'Тестовая страница',
    }
    return render(request, 'lex/test.html', context)


# ============================================
# ФУНКЦИИ ДЛЯ СУДЕБНЫХ ДЕЛ
# ============================================

def case_list(request):
    """Список всех судебных дел"""
    try:
        has_models = True
        cases = Case.objects.all()
        practice_areas = PracticeArea.objects.all()
    except:
        has_models = False
        cases = []
        practice_areas = []

    context = {
        'has_models': has_models,
        'cases': cases,
        'practice_areas': practice_areas,
        'title': 'Судебные дела',
    }
    return render(request, 'lex/case_list.html', context)


def case_detail(request, case_id):
    """Детальная страница судебного дела"""
    case = get_object_or_404(Case, id=case_id)
    context = {
        'case': case,
        'title': f'Дело {case.case_number}',
    }
    return render(request, 'lex/case_detail.html', context)


def practice_areas_list(request):
    """Список всех областей практики"""
    practice_areas = PracticeArea.objects.all()
    context = {
        'practice_areas': practice_areas,
        'title': 'Области юридической практики',
    }
    return render(request, 'lex/practice_areas.html', context)


# ============================================
# ВРЕМЕННЫЕ ФУНКЦИИ (ЗАГОТОВКИ)
# ============================================

def add_case(request):
    """Заготовка для формы добавления дела"""
    context = {
        'title': 'Добавление дела',
    }
    return render(request, 'lex/add_case.html', context)


def edit_case(request, case_id):
    """Заготовка для формы редактирования дела"""
    context = {
        'title': f'Редактирование дела #{case_id}',
        'case_id': case_id,
    }
    return render(request, 'lex/edit_case.html', context)


def search_cases(request):
    """Заготовка для поиска дел"""
    context = {
        'title': 'Поиск дел',
    }
    return render(request, 'lex/search_cases.html', context)


# ============================================
# API ФУНКЦИИ
# ============================================

def api_case_list(request):
    """API список дел"""
    return HttpResponse("API: список дел", content_type="application/json")


def api_case_detail(request, case_id):
    """API детали дела"""
    return HttpResponse(f'{{"id": {case_id}}}', content_type="application/json")


# ============================================
# ТЕСТОВЫЕ ФУНКЦИИ
# ============================================

def test_bootstrap(request):
    """Тестовая страница Bootstrap"""
    context = {
        'title': 'Тест Bootstrap компонентов',
    }
    return render(request, 'lex/test_bootstrap.html', context)


def test_template_tags(request):
    """Тестовая страница тегов шаблонов"""
    news_items = News.objects.filter(is_published=True).order_by('-created_at')[:5]

    context = {
        'title': 'Тест тегов шаблонов',
        'news_items': news_items,
        'test_list': ['Первый', 'Второй', 'Третий', 'Четвертый', 'Пятый'],
    }
    return render(request, 'lex/test_template_tags.html', context)


# ============================================
# КАСТОМНАЯ СТРАНИЦА 404
# ============================================

def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, 'lex/404.html', status=404)


# ============================================
# РЕДИРЕКТЫ С reverse
# ============================================

def redirect_to_category(request, category_id):
    """Редирект на страницу категории"""
    from django.urls import reverse
    url = reverse('lex:news_by_category', kwargs={'category_id': category_id})
    return redirect(url)


def redirect_to_news(request, news_id):
    """Редирект на детальную страницу новости"""
    from django.urls import reverse
    url = reverse('lex:news_detail', kwargs={'pk': news_id})
    return redirect(url)


def redirect_to_home(request):
    """Редирект на главную страницу"""
    from django.urls import reverse
    url = reverse('lex:index')
    return redirect(url)