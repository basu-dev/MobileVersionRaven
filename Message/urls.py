from django.urls import path
from . import views

urlpatterns=[
    path('',views.message_list),
    path('message/<int:id>/',views.chatroom),
    path('save_message/<int:id>/',views.save_message),
]

