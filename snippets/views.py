from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .models import Snippet, Language


class IndexSnippetListView(ListView):
    model = Snippet
    template_name = "index.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(public=True)
        return qs


class SnippetByLanguageDetailView(DetailView):
    model = Language
    template_name = "snippets/language_snippets.html"


class SnippetByUserListView(ListView):
    model = Snippet
    template_name = "snippets/user_snippets.html"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        qs = super().get_queryset().filter(user=user)
        if self.request.user != user:
            qs = qs.exclude(public=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['snippets_creator'] = self.kwargs['username']
        return context


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippets/snippet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = context['object'].language.name
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(full=True, linenos=True, cssclass="source")
        formatted_snippet = highlight(
            context['object'].snippet, lexer, formatter)
        context['formatted_snippet'] = formatted_snippet
        return context


@method_decorator(login_required, name='dispatch')
class SnippetCreateView(CreateView):
    model = Snippet
    template_name = "snippets/snippet_add.html"
    fields = ('name', 'description', 'snippet', 'public', 'language',)
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SnippetUpdateView(UserPassesTestMixin, UpdateView):
    model = Snippet
    template_name = "snippets/snippet_add.html"
    fields = ('name', 'description', 'snippet', 'public', 'language',)
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Guardar cambios'
        return context

    def test_func(self):
        snippet_user = self.get_object().user
        return snippet_user == self.request.user


@method_decorator(login_required, name='dispatch')
class SnippetDeleteView(UserPassesTestMixin, DeleteView):
    model = Snippet
    template_name = "snippets/snippet_confirm_delete.html"
    success_url = reverse_lazy('user_snippets')

    def test_func(self):
        snippet_user = self.get_object().user
        if snippet_user == self.request.user:
            return True
        return False
