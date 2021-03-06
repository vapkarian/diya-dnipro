import random
from diya_dnipro.types import Url

from django.core.urlresolvers import reverse
from django.db.models import QuerySet
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from diya_dnipro.accounts.forms import FeedbackForm
from diya_dnipro.misc.utils import AjaxableResponseMixin
from diya_dnipro.news.models import *


__all__ = [
    'HomeView', 'AllView', 'CategoryView', 'SearchView', 'ArticleView', 'TeamView', 'TeamMemberView', 'DocumentsView',
    'ContactsView',
]


class SectionView(ListView):
    category = None

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.category = get_object_or_404(Category, url=self.kwargs['url'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class HomeView(ListView):
    context_object_name = 'articles'
    http_method_names = ['get']
    template_name = 'news/home.html'

    def get_queryset(self) -> list:
        queryset = Article.objects.filter(is_active=True, is_top=False).order_by('-created')[:15]
        queryset = list(queryset)
        random.shuffle(queryset)
        queryset = sorted(queryset[:6], key=lambda x: x.created, reverse=True)
        return queryset


class AllView(ListView):
    context_object_name = 'articles'
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/all.html'

    def get_queryset(self) -> QuerySet:
        queryset = Article.objects.filter(is_active=True).order_by('-created')
        return queryset


class CategoryView(SectionView):
    context_object_name = 'articles'
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'news/category.html'

    def get_queryset(self) -> QuerySet:
        queryset = Article.objects.filter(category=self.category, is_active=True).order_by('-created')
        return queryset


class SearchView(TemplateView):
    http_method_names = ['get']
    template_name = 'news/search.html'


class ArticleView(DetailView):
    context_object_name = 'article'
    http_method_names = ['get']
    model = Article
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        same = Article.objects \
            .filter(category=self.object.category, is_active=True) \
            .exclude(pk=self.object.pk) \
            .order_by('-created')
        context['same_articles'] = same[:6]
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Article.objects.filter(is_active=True)
        return queryset


class TeamView(SectionView):
    context_object_name = 'members'
    http_method_names = ['get']
    template_name = 'news/team.html'

    def get_queryset(self) -> QuerySet:
        queryset = TeamMember.objects.filter(categories=self.category)
        return queryset


class TeamMemberView(DetailView):
    context_object_name = 'member'
    http_method_names = ['get']
    model = TeamMember
    template_name = 'news/member.html'


class DocumentsView(SectionView):
    context_object_name = 'documents'
    http_method_names = ['get']
    template_name = 'news/documents.html'

    def get_queryset(self) -> QuerySet:
        queryset = Document.objects.filter(categories=self.category).order_by('id')
        return queryset


class ContactsView(AjaxableResponseMixin, CreateView):
    form_class = FeedbackForm
    http_method_names = ['get', 'post']
    template_name = 'news/contacts.html'

    def form_valid(self, form: BaseForm) -> HttpResponse:
        response = super(ContactsView, self).form_valid(form)
        form.send_mail()
        return response

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.order_by('id')
        return context

    def get_success_url(self) -> Url:
        return reverse('news:contacts')
