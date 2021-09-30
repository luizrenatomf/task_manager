from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tasks.urls')),
    path('account/',include('account.urls')),
    path('logs/',include('logs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,decument_root=settings.MEDIA_ROOT)
