from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index, name='register_login'),
    path('wishes', views.dashboard, name='dashboard'),
    path('add_wish', views.add_wish, name='add_wish'),
    path('make_add', views.make_wish, name='make_add'),
    path('view_stats', views.view_stats, name='view_stats'),
    path('remove_wish/<int:wish_id>', views.remove_wish, name='remove_wish'),
    path('edit_wish/<int:wish_id>', views.edit_wish, name='edit_wish'),
    path('make_edit/<int:wish_id>', views.make_edit, name='make_edit'),
    path('grant_wish/<int:wish_id>', views.grant_wish, name='grant_wish'),
    path('like_wish/<int:wish_id>',views.like_wish, name='like_wish'),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout, name='logout')
]