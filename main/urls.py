
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('aaddmmiinn/', admin.site.urls),
    path('', include('forum.urls')),
]

error_404 = 'forum.views.error_404'
error_500 = 'forum.views.error_500'
