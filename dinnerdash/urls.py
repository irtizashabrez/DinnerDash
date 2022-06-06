from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from dinnerdash.settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls')),
    path('', include('authentications.urls')),
    path('', include('orders.urls')),
]
