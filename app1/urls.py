from django.urls import path
from . import views 

app_name = 'app1'

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('ideas/', views.ideas, name='ideas'),
    path('team/', views.team, name='team'),
    path('add-idea', views.add_idea, name='add_idea'),
    path('create-team/', views.create_team, name='create_team'),
    path('join-team', views.join_team, name='join_team'),
    path('delete-idea/<int:pk>/', views.delete_idea, name='delete_idea'),
    path('edit-idea/<int:pk>/', views.edit_idea, name='edit_idea'),
    path('user_ideas/<int:pk>/', views.user_ideas, name='user_ideas'),
]

