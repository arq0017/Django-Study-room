from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('register/', views.register_user, name='register-user'),
    path('logout/', views.logout_user, name='logout-user'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),

    path('profile/<str:user_id>', views.user_profile, name='user-profile'),
    path('edit_profile/', views.edit_profile, name='edit-profile'),

    path('create_room/', views.create_room, name='create-room'),
    path('update_room/<str:room_id>', views.update_room, name='update-room'),
    path('delete_room/<str:room_id>', views.delete_room, name='delete-room'),

    path('delete_comment/<str:room_id>/<str:comment_id>',
         views.delete_comment, name='delete-comment'),

    path('topics/', views.topic_page, name='topics'),
    path('activity/', views.activity_page, name='activities'),
] 
