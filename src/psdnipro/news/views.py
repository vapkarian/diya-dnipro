import random

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from psdnipro.accounts.forms import FeedbackForm
from psdnipro.misc.search import get_query
from psdnipro.misc.utils import AjaxableResponseMixin
from psdnipro.news.models import *


__all__ = [
    'HomeView', 'CategoryView', 'SearchView', 'ArticleView', 'TeamView', 'TeamMemberView', 'DocumentsView',
    'ContactsView',
]


class SectionView(ListView):
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, is_active=True, url=self.kwargs['url'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class HomeView(ListView):
    context_object_name = 'articles'
    http_method_names = ['get']
    template_name = 'news/home.html'

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True, is_top=False).order_by('-created')[:15]
        queryset = list(queryset)
        random.shuffle(queryset)
        queryset = sorted(queryset[:6], key=lambda x: x.created, reverse=True)
        return queryset


class CategoryView(SectionView):
    context_object_name = 'articles'
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/category.html'

    def get_queryset(self):
        queryset = Article.objects.filter(category=self.category, is_active=True).order_by('-created')
        return queryset


class SearchView(ListView):
    context_object_name = 'articles'
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/search.html'
    search_query = None

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    context_object_name = 'article'
    http_method_names = ['get']
    model = Article
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        same = Article.objects \
            .filter(category=self.object.category, is_active=True) \
            .exclude(pk=self.object.pk) \
            .order_by('-created')
        context['same_articles'] = same[:6]
        return context

    def get_queryset(self):
        queryset = Article.objects.filter(is_active=True)
        return queryset


class TeamView(SectionView):
    context_object_name = 'members'
    http_method_names = ['get']
    template_name = 'news/team.html'

    def get_queryset(self):
        queryset = TeamMember.objects.filter(categories=self.category, is_active=True).order_by('id')
        return queryset


class TeamMemberView(DetailView):
    context_object_name = 'member'
    http_method_names = ['get']
    model = TeamMember
    template_name = 'news/member.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


class DocumentsView(SectionView):
    context_object_name = 'documents'
    http_method_names = ['get']
    template_name = 'news/documents.html'

    def get_queryset(self):
        queryset = Document.objects.filter(category=self.category, is_active=True).order_by('id')
        return queryset


class ContactsView(AjaxableResponseMixin, CreateView):
    form_class = FeedbackForm
    http_method_names = ['get', 'post']
    template_name = 'news/contacts.html'

    def form_valid(self, form):
        response = super(ContactsView, self).form_valid(form)
        form.send_mail()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.filter(is_active=True)
        return context

    def get_success_url(self):
        return reverse('news:contacts')
