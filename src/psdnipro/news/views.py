from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView, DetailView

from psdnipro.news.models import Article, Category, TeamMember


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


class TeamView(ListView):
    http_method_names = ['get']
    template_name = 'news/team.html'
    context_object_name = 'team_members'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, url=self.kwargs['url'])
        return super(TeamView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        qs = TeamMember.objects.filter(category=self.category).order_by('id')
        return qs


class TeamMemberView(DetailView):
    http_method_names = ['get']
    model = TeamMember
    template_name = 'news/member.html'
