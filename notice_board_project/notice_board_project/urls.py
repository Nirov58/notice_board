from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from ckeditor_uploader.views import upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign/', include('notice_board_sign_app.urls')),
    path('responses/', include('notice_board_protection_app.urls')),
    path('posts/', include('notice_board_main_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
