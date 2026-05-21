# lex/forms.py
from django import forms
from .models import News, PracticeArea


class NewsForm(forms.ModelForm):
    """
    Форма для редактирования новости (связанная с моделью News)
    Вариант 14: Редактирование через форму
    """

    class Meta:
        model = News
        # Явно указываем поля (не используем '__all__' - плохая практика)
        fields = ['title', 'content', 'category', 'is_published', 'photo']

        # Русские метки для полей
        labels = {
            'title': 'Заголовок новости',
            'content': 'Содержание новости',
            'category': 'Категория',
            'is_published': 'Опубликовано',
            'photo': 'Изображение',
        }

        # Настройка виджетов для Bootstrap 5
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок новости'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Введите текст новости'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Дополнительная настройка формы
        """
        super().__init__(*args, **kwargs)
        # Делаем поле content обязательным (по умолчанию оно обязательное)
        self.fields['content'].required = True
        # Настройка выпадающего списка категорий
        self.fields['category'].empty_label = "Выберите категорию"
        self.fields['category'].queryset = PracticeArea.objects.all().order_by('name')