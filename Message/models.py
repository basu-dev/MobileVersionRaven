from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    body = models.TextField()
    seen = models.BooleanField(default = False)
    delete_by_sender = models.IntegerField(default=0)
    delete_by_receiver = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    def get_sender(self):
        sender=User.objects.get(id =self.sender)
        return sender
    def get_receiver(self):
        receiver=User.objects.get(id =self.receiver)
        return receiver

def get_last_n_messages_with(u_id,id,n,all=False):
    messages =[]
    if all:
        messages=Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(delete_by_sender = u_id)|Q(delete_by_receiver=u_id)).exclude(Q(sender=u_id) & Q(receiver=u_id))
    else:
        try:
            messages=Message.objects.filter(Q(sender=u_id)|Q(receiver=u_id)).filter(Q(sender=id)|Q(receiver=id)).exclude(Q(delete_by_sender = u_id)|Q(delete_by_receiver=u_id)).order_by('-id')[:n]
        except:
            i=0    
    if messages:
        for message in messages:
            if message.sender is u_id:
                message.user= User.objects.get(id = u_id)
                message.receiver=User.objects.get(id=id)
            else:
                message.user= User.objects.get(id = id)
                message.receiver=User.objects.get(id=id)
        messages=set(messages)
        return messages
          

