from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def index(request,*args, **kwargs):
    
    
    return render(request, 'index.html', {})

def chat_room(request, *args, **kwargs):
    room_name = kwargs.get('username')
    context = {
        'room_name': room_name,
    }
    return render(request, 'chat.html', context)  
    
      
