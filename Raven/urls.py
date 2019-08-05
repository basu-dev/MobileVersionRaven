from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Message.urls')),
    path('login/',views.login_view),
    path('signup/',views.signup),
    path('logout/',views.log_out),
    path('setting/',include('Friend.urls')),
    path('story/',include('Story.urls')),
    path('make_me_online/',views.update_online),
    path('update_status/',views.update_state),
    path('notifyme/',views.notifyme),
    path('new_message/<int:id>/',views.new_message),
    path('message/new_message/',views.new_message_home),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)