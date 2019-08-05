from django.shortcuts import render,redirect,HttpResponse
from Message.models import *
from Friend.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import random
from django.utils import timezone
import datetime
from Story.models import *
from django.http import JsonResponse

@login_required(login_url='/login/')
def new_message(request,id):
    try:
        new_message=Message.objects.filter(receiver=request.user.id).filter(sender=id).filter(seen=False)[0]
    except:
        new_message=0
    if new_message:
        respon={'state':'changed','message':new_message.body}
        new_message.seen=True
        new_message.save()
    else:
        respon={'state':'unchanged'}        
    return JsonResponse(respon)

@login_required(login_url='/login/')
def notifyme(request):
    try:
        notification=Notification.objects.filter(seen=False).filter(user=request.user).last()
        notification.seen=True
        notification.save()
    except:
        notification=0
    if notification:
        noti={'state':'changed','url':notification.url,'body':notification.body}
        return JsonResponse(noti)
    else:
        noti={'state':'nochanged'}
        return JsonResponse(noti)

@login_required(login_url='/login/')
def update_state(request):
    state=request.GET['state']
    online_user=Online.objects.get(user=request.user)
    if state=='true':
        online_user.date=datetime.datetime.now()
        online_user.is_turned_off=True
    else:
        online_user.date=datetime.datetime.now()
        online_user.is_turned_off=False
    online_user.save()
    return HttpResponse('hide')
    
@login_required(login_url='/login/')
def update_online(request):
    try:
        online_user=Online.objects.get(user=request.user)
       
        
        if online_user:
            if online_user.is_turned_off:
                return HttpResponse('online mode turned off')
            else:
                online_user.last_seen=datetime.datetime.now()
                online_user.save()
        else:
            online_use=Online()
            online_use.user=request.user
            online_use.last_seen=timezone.now()
            online_use.save()
        return HttpResponse('true')
    except:
        online_user=0

@login_required(login_url='/login/')
def message_list(request):
    messages=[]
    mero_sathiharu=get_all_friends_user(request.user.id)
    for euta_sathi in mero_sathiharu:
        messages+=list(get_last_n_messages_with(request.user.id,euta_sathi.id,1))
    
    request.notification=get_last_ten(request.user)
    return render(request,'message.html',{'messages':messages})

class formerror():
    def __init__(self):
        self.username_error=''
        self.password_error=''
        self.name_error=''

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    fe=formerror()
    ne=''
    pe=''
    ue=''
    newuser=User()
    if request.method=='POST':
        newuser.username=request.POST['username']
        newuser.password1=request.POST['password1']
        newuser.password2=request.POST['password2']
        newuser.first_name=request.POST['first_name']
        newuser.last_name=request.POST['last_name']
        validation=1
        if newuser.password1==newuser.password2:
            if len(newuser.password1)<6:
                fe.password_error='Password must be grater than 6 digits!'
                pe='is-invalid'
                validation=0
                 
        else:
            fe.password_error='Two password didnot match!'
            pe='is-invalid'
            validation=0
        try:
            user=User.objects.filter(username=newuser.username).get()
        except:
            user=0
            ue='is-valid' 
        if user:
            fe.username_error='User already exits!'
            validation=0
            ue='is-invalid'
        if newuser.first_name and newuser.last_name:
            v=1
        else :
            validation=0
            fe.name_error='First and last name is required!'
            ne='is-invalid'
        if validation:
            newuser.set_password(newuser.password1)
            newuser.save()
            return redirect('/login/')
        else:
            return render(request,'account/signup_view.html',{'page_title':'signup-ElectronisHub','formerror':fe,'username':ue,'password':pe,'first_name':ne,'data':newuser})

    else:
        return render(request,'account/signup_view.html',{'page_title':'signup-ElectronisHub','formerror':fe})

def login_view(request):
    fe=formerror()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            fe.message='Username/password error please provede correct credentials'
            return render(request,'account/login_view.html',{'page_title':'Login-ElectronicsHub','formerror':fe})  
    else:
        return render(request,'account/login_view.html',{'page_title':'Login-ElectronicsHub','formerror':fe}) 

@login_required(login_url='/login/')
def search(request):         
    friend_list = get_all_friends_user(request.user.id)
    request_list=[]
    friend_request=Friend_request.objects.filter(receiver=request.user.id)
    for i in friend_request:
        request_list+=User.objects.filter(id=i.sender)
    friend_suggestion=[]
    suggestion=[]
    count=[]
    my_friend=get_all_friends_user(request.user.id)
    for i in my_friend:
        i.friends=get_all_friends_user(i.id)
        suggestion+=set(i.friends)-set(my_friend)
        for j in suggestion:
            if j.id is not i.id:
                friend_suggestion+=User.objects.filter(id=j.id)
    friend_suggestion=list(dict.fromkeys(friend_suggestion))
    if friend_suggestion:
        friend_suggestion.remove(request.user)
        for k in friend_suggestion:
            k.mutual=get_mutual_friends(request.user.id,k.id)
        random.shuffle(friend_suggestion)

    else:
        friend_suggestion+=User.objects.filter(id=1)
    try:
        searchdata=request.GET['search_query']
        if searchdata:
            users=User.objects.filter(Q(username__contains=searchdata) |Q(first_name__contains=searchdata) | Q(last_name__contains=searchdata)).exclude(id=request.user.id)
            for i in users:
                i.friend=Friend.objects.filter(Q(sender=request.user.id) |Q(sender=i.id)).filter(Q(receiver=request.user.id) |Q(receiver=i.id))
                if i.friend:
                    i.is_my_friend=True
                else:
                    i.is_my_friend=False
    except:
        user=0
    request.notification=get_last_ten(request.user)
    return render(request,'search.html',{'users':users,'friend_suggestion':friend_suggestion,'friend_list':friend_list,'request_sender':request_list})

@login_required(login_url='/login/')
def log_out(request):

    if request.method=='POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/login/')
        else:
            return redirect('/login/') 
    else:
        return redirect('/login/')    

@login_required(login_url='/login/')
#for notificaiton

def new_message_home(reqeust):
    new_message=Message.objects.filter(receiver=reqeust.user.id)
    if new_message:
        a='True'
    else:
        a='False'    
    JsonResponse({'status':a})