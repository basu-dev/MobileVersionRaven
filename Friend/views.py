from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Friend.models import *
from Story.models import *

def setting(request):
    try:
        request.notification=get_last_ten(request.user)
        request.onlinestatus=Online.objects.get(user=request.user).get_last_seen()
        status=Online.objects.get(user=request.user)
        if status.is_turned_off:
            request.status='checked'
        return render(request,'setting.html')
    except:
        return render(request,'setting.html')

@login_required(login_url='/login/')
def active_list(request):
    friend_list=[]
    active_list=[]
    offline_list=[]
    friend_list=get_all_friends_user(request.user.id)

    if friend_list:
        for friend in friend_list:
            try:
                active=Online.objects.get(user=friend).is_online()
                if active:
                    active_list+=User.objects.filter(id=friend.id)
                else:
                    offline_list+=User.objects.filter(id=friend.id)
            except:
                pass
    request.notification=get_last_ten(request.user)
    return render(request,'online_user.html',{'active_friends':active_list,'offline_friends':offline_list})        




