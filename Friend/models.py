from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Friend_request(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    
def request_sender(id):
    request_sender = Friend_request.objects.filter(Q(sender = id)|Q(receiver = id))
    if request_sender:
        return request_sender

class Friend(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    is_blocked = models.IntegerField(default=0)

def get_all_friends_user(id):
    friends = Friend.objects.filter(Q(sender = id) | Q(receiver = id)).filter(is_blocked = 0)
    friend_list=[]
    for i in friends:
        if i.sender is not id:
            friend_list+=User.objects.filter(id=i.sender)
        else:
            friend_list+=User.objects.filter(id=i.receiver)
    return friend_list

def get_mutual_friends(id,sid):
    mero_friends=list(get_all_friends_user(id))
    usko_sathi=list(get_all_friends_user(sid))
    a=len([element for element  in mero_friends if element in usko_sathi])
    return a

class Profile(models.Model):
    profile_picture = models.ImageField(upload_to = 'user-profile/')
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    age = models.IntegerField()
    job = models.CharField(max_length = 100)
    bio = models.TextField()
    address = models.CharField(max_length = 100)
    contack_no = models.CharField(max_length=15)

import datetime
from django.utils import timezone

class Online(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)
    is_turned_off=models.BooleanField(default=0)

    def is_online(self):
        now=timezone.now()
        duration=now-self.last_seen
        totalsec= duration.seconds
        if totalsec <20:
            return True
        else:
            return False
    def get_last_seen(self):
        anow= timezone.now()
        duration=anow-self.last_seen
        duration_in_s = duration.seconds
        years = int(duration_in_s/31556926)
        days  = int(duration_in_s/ 86400)
        hours = int(duration_in_s/3600)
        minutes = int(duration_in_s/60)
        if years:
            return 'last seen on '+str(self.last_seen)
        elif days:
            return 'last seen '+str(days)+' days ago'
        elif hours:
            return 'last seen '+str(hours)+' hours ago'
        else:
            if duration_in_s>59:
                return 'last seen '+str(minutes)+' minutes ago'
            elif duration_in_s>20:
                return 'last seen '+str(duration_in_s)+'seconds  ago ago'  
            else:
                return 'online'  







    
