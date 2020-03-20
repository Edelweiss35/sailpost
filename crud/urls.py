from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.fileupload, name='index'),
    # url('fileupload',views.fileupload, name='fileupload'),
    url(r'^create-user/$', views.register,name='register'),
    url(r'^create-user/success/$',views.register_success,name='register_success'),
    url(r'^users/$',views.users,name='users'),
    url(r'^users/delete/(?P<id>\d+)$', views.user_delete, name='user_delete'),
    url(r'^change_password$', views.changePassword, name='changePassword'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)