from django.urls import path
from . import views

app_name = 'chat'


urlpatterns = [
    path('<str:username>/', views.chat_room, name='chat_room'),
    
]
