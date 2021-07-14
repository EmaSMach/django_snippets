from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .models import Snippet


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    return render(request, 'login.html', {})


class IndexSnippetListView(ListView):
    model = Snippet
    template_name = "index.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(public=True)
        if self.request.user.is_authenticated:
            qs = qs.all()
        return qs

# def index(request):
#     return render(request, 'index.html', {})


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

class SnippetCreateView(CreateView):
    model = Snippet
    template_name = "snippets/snippet_add.html"
    fields = '__all__'
    exclude = ['user',]
    success_url = reverse_lazy('index')

# def snippet_add(request):
    # return render(request, 'snippets/snippet_add.html', {})


class SnippetUpdateView(UpdateView):
    model = Snippet
    template_name = "snippets/snippet_add.html"
    fields = '__all__'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Guardar cambios'
        return context

# def snippet_edit(request):
#     return render(request, 'snippets/snippet_add.html', {})

class SnippetDeleteView(DeleteView):
    model = Snippet
    template_name = "snippets/snippet_confirm_delete.html"
    success_url = reverse_lazy('user_snippets')

# def snippet_delete(request):
#     return render(request, 'snippets/user_snippets.html', {})
