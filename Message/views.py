from django.shortcuts import render,redirect,HttpResponse
from Message.models import *
from Friend.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import random
from django.http import JsonResponse
from Story.models import *
import datetime
@login_required(login_url='/login/')
def message_list(request):
    try:
        online_user=Online.objects.filter(user=request.user)
    except:
        online_user=0
    if online_user:
        pass
    else:
        online_user=Online()
        online_user.user=request.user
        online_user.date=datetime.datetime.now()
        online_user.save()   
    
    messages=[]
    try:
        mero_sathiharu=get_all_friends_user(request.user.id)
    except:
        i=0
    for euta_sathi in mero_sathiharu:
        try:
            messages+=get_last_n_messages_with(request.user.id,euta_sathi.id,1)
        except:
            i=0  
        #messages+=get_last_n_messages_with(request.user.id,3,1)
    for msg in messages:
        msg.user.activestatus= Online.objects.get(user=msg.receiver).is_online()
    request.notification=get_last_ten(request.user)    
    return render(request,'message.html',{'messages':messages})
@login_required(login_url='/login/')
def chatroom(request,id):
    request.notification=get_last_ten(request.user)
    try:
        user=User.objects.get(id=id)
    except:
        user=0
    if user:
        messages=[]
        messages=get_last_n_messages_with(request.user.id,id,25)
        if messages:
            for message in messages:
                if message.sender == id:
                    message.rcvr=True

        return render(request,'chatroom.html',{'messages':messages,'receiver':user}) 

@login_required(login_url='/login/')
def save_message(request,id):
    if request.method=='POST':
        if request.is_ajax():
            message=Message()
            message.sender=request.user.id
            message.receiver=id
            message.body=request.POST['message']
            if message.body:
                message.save()
                respon={'state':'saved'}
            else:
                 respon={'state':'not saved'}
        return JsonResponse(respon)         

    elif request.method=='POST':
        message=Message()
        message.sender=request.user.id
        message.receiver=id
        message.body=request.POST['message']
        message.save()
        return redirect('/message/'+str(id))