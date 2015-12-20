from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView, DetailView

from psdnipro.news.models import Article, Category


__all__ = [
    'HomeView', 'CategoryView', 'ArticleView'
]


class HomeView(ListView):
    http_method_names = ['get']
    template_name = 'news/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        qs = Article.objects.filter(is_active=True).order_by('-created')[:6]
        return qs


class CategoryView(ListView):
    http_method_names = ['get']
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, url=self.kwargs['url'])
        return super(CategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        qs = Article.objects.filter(category=self.category, is_active=True).order_by('-created')
        return qs


class ArticleView(DetailView):
    http_method_names = ['get']
    model = Article
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        same = Article.objects.filter(category=self.object.category, is_active=True).order_by('-created')[:6]
        context['same_articles'] = same
        return context
