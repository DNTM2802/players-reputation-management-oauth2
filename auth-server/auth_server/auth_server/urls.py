from django.contrib import admin
from django.urls import path, include
from auth_server.views import *
from auth_server.views.mvt.protected.views import profile_view, logout_view, change_password_view
from auth_server.views.mvt.public.views import login_view, login_cmd_view, login_cmd_callback_view, register_cmd_view, \
    register_cmd_callback_view, register_credentials_view
from auth_server.views.rest.protected.views import rw_reputation

urlpatterns = [
    path('', profile_view, name='profile'),
    #path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/login_cmd/', login_cmd_view, name='login_cmd'),
    path('accounts/login_cmd_callback/', login_cmd_callback_view, name='login_cmd_callback'),
    path('accounts/change_password/', change_password_view, name='change_password'),
    path('register/', register_cmd_view, name='register'),
    path('register_cmd_callback/', register_cmd_callback_view, name='register_cmd_callback'),
    path('register_credentials/', register_credentials_view, name='register_credentials'),
    path('api/reputation', rw_reputation, name='rw_reputation'), # Protected resource
]
