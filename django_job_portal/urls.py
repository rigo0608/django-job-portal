
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),
    path('', include('django.contrib.auth.urls')),  # <-- this line is important
]


