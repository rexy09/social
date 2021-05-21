from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

# class PublicChatRoom(models.Model):
# 	title = models.CharField(max_length=255, unique=True)
# 	users = models.ManyToManyField(User,related_name='public_chat_room', help_text='User connected to chat.')
# 	updated_at = models.DateTimeField(auto_now=True)
# 	created_at = models.DateTimeField(auto_now_add=True) 
	
# 	def __str__(self):
# 		return self.title

# 	def connect_user(self, user):
# 		is_user_added = False

# 		if not user in self.users.all():
# 			self.users.add(user)
# 			self.save()
# 			is_user_added = True
# 		elif user in self.users.all():	
# 			is_user_added = True
# 		return is_user_added	


# 	def disconnect_user(self, user):
# 		is_user_removed = False

# 		if user in self.users.all():
# 			self.users.remove(user)
# 			self.save()
# 			is_user_removed = True		
# 		return is_user_removed	

# 	@property
# 	def group_name(self):
# 		return f'PublicChatRoom-{self.id}'		

					
# 	class Meta:
# 		verbose_name = 'PublicChatRoom'
# 		verbose_name_plural = 'PublicChatRooms'


class Thread(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable = False)
	members      = models.ManyToManyField(User, related_name='chat_thread', blank=True,)
	created      = models.BooleanField(default=False)
	updated      = models.DateTimeField(auto_now=True)
	timestamp    = models.DateTimeField(auto_now_add=True)    
	

class Message(models.Model):
	thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
	user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
	message     = models.TextField()
	is_readed   = models.BooleanField(default=False)
	timestamp   = models.DateTimeField(auto_now_add=True)
