from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter

from django.forms.widgets import DateInput, CheckboxSelectMultiple

from .models import Post, Category, Response


class PostFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Заголовок')
    date = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gte',
        label='Не позднее даты'
    )
    author__username = CharFilter(lookup_expr='icontains', label='Автор')
    categories = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(),
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['categories', 'name', 'author__username', 'date']


class ResponseFilter(FilterSet):
    user = None
    author__username = CharFilter(lookup_expr='icontains', label='Отправитель')
    date = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gte',
        label='Не позднее даты'
    )
    target__name = CharFilter(lookup_expr='icontains', label='Объявление')

    class Meta:
        model = Response
        fields = ['target__name', 'author__username', 'date']
