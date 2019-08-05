from django.shortcuts import render,redirect,HttpResponse
from Story.models import *
from Message.models import *
from django.contrib.auth.decorators import login_required
from Friend.models import *
from django.http import JsonResponse
@login_required(login_url='/login/')
def storyline(request):
    friend_list=[]
    stories=[]
    mero_stories=[]
    friend_list = get_all_friends_user(request.user.id)
    for i in friend_list:
        stories+=Post.objects.filter(user=i).order_by('-id')
    for i in stories:
        i.comment=get_comment(i.id)
        i.comment.count=i.comment.count()
        if i.comment.count>2:
            i.is_grt_thn_two=True
    for story in stories:
        story.like = Like.objects.filter(post = story)
        story.if_liked=Like.objects.filter(post = story).filter(user=request.user)
        if story.if_liked:
            story.is_liked='Liked'
        else:
            story.is_liked='Like'
        
    mero_stories+=Post.objects.filter(user=request.user.id).order_by('-id')
    for i in mero_stories:
        i.comment=get_comment(i.id)
        i.comment.count=i.comment.count()
        if i.comment.count>2:
            i.is_grt_thn_two=True
    for i in mero_stories:
        i.like=Like.objects.filter(post=i)
        i.if_liked=Like.objects.filter(post=i).filter(user=request.user)
        if i.if_liked:
            i.is_liked='Liked'
        else:
            i.is_liked='Like'    
        
    request.notification=get_last_ten(request.user)
    
    return render(request,'stories.html',{'stories':stories,'mero_stories':mero_stories})
@login_required(login_url='/login/')
def save_comment(request, id):
    if request.method=='POST':
        comment = request.POST['comment']
        new_cmt = Comment()
        new_cmt.body= comment
        new_cmt.user =  request.user
        new_cmt.post  = Post.objects.get(id = id)
    
        if comment:
            set_notification(new_cmt.post.user,request.user.username +' commented on your post :'+comment ,0,'/profile/')
            new_cmt.save()
        
        return redirect('/story/')
    else:
        return redirect('/story')

@login_required(login_url='/login/')
def save_like(request, id):
    if request.is_ajax() and request.method=='POST':
        post =Post.objects.get(id = id)
        try:
            like=Like.objects.filter(post=post).filter(user=request.user)
        except:
            like=0
        if like:
            like.delete()
            is_liked='Like'
            c=Like.objects.filter(post=post).count()
        else:
            like=Like()
            like.like=1
            like.user=request.user
            like.post=post
            like.save()
            set_notification(post.user, request.user.first_name+' '+request.user.last_name +' liked your post.',0,'/profile/')
            c=Like.objects.filter(post=post).count()
            is_liked='Liked'
        id=post.id    
        return JsonResponse({'count':c,'is_liked':is_liked,'id':id})
    elif request.method=='POST':
       post =Post.objects.get(id = id)
       try:
           like=Like.objects.filter(user=request.user).filter(post=post)
       except:
            like=0  
       if like:
           like.delete()
           try:
               link=request.POST['redirect_to']
           except:
                link=0
           if link:
                return redirect(link)
           else:
                return redirect('/')
       else:
            link=request.POST['redirect_to']
            newlike=Like()
            newlike.user=request.user
            newlike.post=post
            newlike.like=True
            newlike.save()
            set_notification(post.user, request.user.first_name+' '+request.user.last_name +' liked your post.',0,'/profile/')
            return redirect(link)
    else:
        return redirect('/')        

def add_story(request):

    if request.method=='POST':
        post=request.POST['add_story']
        if post:
            new_story=Post()
            new_story.user=request.user
            new_story.body=request.POST['add_story']
            new_story.save()
            return redirect('/story/')

@login_required(login_url='/login')
def delete_story(request,id):
   if request.is_ajax:
       if request.method == 'POST':
           post=Post.objects.filter(user=request.user).get(id=id)
           if post.user==request.user:
               post.delete()
               post.is_deleted='True'
               a=post.is_deleted
               return JsonResponse({'data':a})            
            


