from django.contrib import admin
from django.urls import include, path
from fantasy_realms.main import urls
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include(urls)),
    path('api-token-auth/', views.obtain_auth_token)]

print('s')