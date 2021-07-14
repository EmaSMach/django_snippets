from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .models import Snippet


# def login(request):
#     return render(request, 'login.html', {})


# def logout(request):
#     return render(request, 'login.html', {})


class IndexSnippetListView(ListView):
    model = Snippet
    template_name = "index.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(public=True)
        return qs

# def index(request):
#     return render(request, 'index.html', {})

class SnippetByLanguageListView(ListView):
    model = Snippet
    template_name = ".html"

def language(request):
    return render(request, 'index.html', {})


def user_snippets(request):
    return render(request, 'snippets/user_snippets.html', {})


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippets/snippet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = context['object'].language.name
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(full=True, linenos=True, cssclass="source")
        formatted_snippet = highlight(context['object'].snippet, lexer, formatter)
        context['formatted_snippet'] = formatted_snippet
        return context

# def snippet(request):
#     return render(request, 'snippets/snippet.html', {})

@method_decorator(login_required, name='dispatch')
class SnippetCreateView(CreateView):
    model = Snippet
    template_name = "snippets/snippet_add.html"
    fields = ('name', 'description', 'snippet', 'public', 'language',)
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            # form.save()
        return super().form_valid(form)

# def snippet_add(request):
    # return render(request, 'snippets/snippet_add.html', {})

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
            # return True
        # return False

# def snippet_edit(request):
#     return render(request, 'snippets/snippet_add.html', {})

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

# def snippet_delete(request):
#     return render(request, 'snippets/user_snippets.html', {})
