from django.db.models import QuerySet
from django.views.generic import ListView, DetailView

from diya_dnipro.shop.models import Category, Item


__all__ = [
    'MainView', 'CategoryView', 'ItemView',
]


class MainView(ListView):
    context_object_name = 'items'
    http_method_names = ['get']
    paginate_by = 6
    template_name = 'shop/main.html'

    def get_queryset(self) -> QuerySet:
        # TODO: ordering
        queryset = Item.objects.filter(is_best=True)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryView(ListView):
    pass


class ItemView(DetailView):
    pass
