from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from post.views import index, post, blog, search

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('search/', search, name="search"),
    path('blog/', blog, name="post-list"),
    path('post/<id>/', post, name="post-detail"),
    path('tinymce/', include('tinymce.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
