from django.urls import path
from . import views

urlpatterns=[
    path('',views.storyline),
    path('comment/<int:id>/',views.save_comment),
    path('like/<int:id>/',views.save_like),
    path('add_story/',views.add_story),
    path('delete/<int:id>/',views.delete_story),
  
]