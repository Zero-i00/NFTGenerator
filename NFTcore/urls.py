from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path, include
from django.conf.urls.static import static
from NFTGenerator import settings
from .views import *



urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('create_collections/', FileFieldView.as_view(), name='create_collections'),
    # path('collection-preview/', PreviewView.as_view(), name='collection-preview'),
    path('download-img/', GeneratedImageView.as_view(), name='download-img'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)