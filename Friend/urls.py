from django.urls import path
from . import views

urlpatterns=[
    path('',views.setting),
    path('online_users/',views.active_list),
]