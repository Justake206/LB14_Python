# lex/mixins.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PaginationMixin:
    """
    Миксин для добавления пагинации с кастомными настройками.
    Не зависит от конкретной модели - универсальный.
    """
    # Количество объектов на страницу по умолчанию
    paginate_by = 10

    # Имя GET-параметра для страницы
    page_kwarg = 'page'

    # Минимальное количество объектов на последней странице
    paginate_orphans = 0

    # Разрешать пустую первую страницу
    allow_empty_first_page = True

    def get_paginate_by(self, queryset):
        """
        Возвращает количество объектов на страницу.
        Можно переопределить для динамического значения.
        """
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        """
        Возвращает экземпляр пагинатора.
        """
        return Paginator(queryset, per_page, orphans, allow_empty_first_page)

    def paginate_queryset(self, queryset, page_size):
        """
        Пагинирует queryset и возвращает кортеж (paginator, page, page_objects, is_paginated).
        """
        paginator = self.get_paginator(queryset, page_size, self.paginate_orphans, self.allow_empty_first_page)

        page_number = self.request.GET.get(self.page_kwarg, 1)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # Если номер страницы не целое число - показываем первую
            page = paginator.page(1)
        except EmptyPage:
            # Если страница вне диапазона - показываем последнюю
            page = paginator.page(paginator.num_pages)

        return (paginator, page, page.object_list, page.has_other_pages())

    def get_context_data(self, **kwargs):
        """
        Добавляет данные пагинации в контекст.
        """
        context = super().get_context_data(**kwargs)

        # Добавляем информацию о пагинации
        if hasattr(self, 'paginator'):
            context['paginator'] = self.paginator
            context['page_obj'] = self.page_obj
            context['is_paginated'] = self.page_obj.has_other_pages()
            context['current_page'] = self.page_obj.number
            context['total_pages'] = self.paginator.num_pages

            # Добавляем диапазон страниц для отображения (по 2 с каждой стороны)
            current = self.page_obj.number
            page_range = list(self.paginator.page_range)

            # Показываем текущую страницу и по 2 соседних
            context['display_pages'] = [
                p for p in page_range
                if abs(p - current) <= 2 or p <= 2 or p >= self.paginator.num_pages - 1
            ]

        return context