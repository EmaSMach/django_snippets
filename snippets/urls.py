from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.IndexSnippetListView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('snippets/user/<str:username>/', views.SnippetByUserListView.as_view(), name='user_snippets'),
    path('snippets/<int:pk>/', views.SnippetDetailView.as_view(), name='snippet'),
    path('snippets/add/', views.SnippetCreateView.as_view(), name='snippet_add'),
    path('snippets/<int:pk>/edit/', views.SnippetUpdateView.as_view(), name='snippet_edit'),
    path('snippets/<int:pk>/delete/', views.SnippetDeleteView.as_view(), name='snippet_delete'),
    path('snippets/<slug:slug>/', views.SnippetByLanguageDetailView.as_view(), name='language'),
]
