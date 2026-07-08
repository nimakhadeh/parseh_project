from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail'),  # مسیر جدید برای جزئیات ملک
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
