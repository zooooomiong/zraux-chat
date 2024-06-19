from django.urls import path
from .views import register, chat, messages, send_message, login, index, online_users

urlpatterns = [
    path("", index, name="index"),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('chat/', chat, name='chat'),
    path('messages/', messages, name='messages'),
    path('send_message/', send_message, name='send_message'),
    path("onlineusers/", online_users, name="onlineusers")
]
