from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from psdnipro.misc.search import get_query
from psdnipro.news.models import Article, Category, TeamMember


__all__ = [
    'HomeView', 'CategoryView', 'SearchView', 'ArticleView', 'TeamView', 'TeamMemberView',
]


class HomeView(ListView):
    http_method_names = ['get']
    template_name = 'news/home.html'

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True).order_by('-created')[:6]
        return queryset


class CategoryView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/category.html'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, url=self.kwargs['url'])
        return super(CategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = Article.objects.filter(category=self.category, is_active=True).order_by('-created')
        return queryset


class SearchView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/search.html'
    search_query = None

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search', '')
        print(self.request.GET.urlencode())
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['search_query'] = self.search_query
        return context

    def get_queryset(self):
        search_query = self.search_query
        entry_query = get_query(search_query, ['title', 'text'])
        queryset = Article.objects.filter(is_active=True).order_by('-created')
        if entry_query is None:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(entry_query).distinct()
        return queryset


class ArticleView(DetailView):
    http_method_names = ['get']
    model = Article
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        same = Article.objects \
            .filter(category=self.object.category, is_active=True) \
            .exclude(pk=self.object.pk) \
            .order_by('-created')
        context['same_articles'] = same[:6]
        return context

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True)
        return queryset


class TeamView(ListView):
    context_object_name = 'team_members'
    http_method_names = ['get']
    template_name = 'news/team.html'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, url=self.kwargs['url'])
        return super(TeamView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeamView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = TeamMember.objects.filter(category=self.category).order_by('id')
        return queryset


class TeamMemberView(DetailView):
    http_method_names = ['get']
    model = TeamMember
    template_name = 'news/member.html'
