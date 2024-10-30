
from django.contrib import admin
from django.urls import path

from users.views import about_us, activate_account, get_file, get_file_name, get_jwt_token_from_cookie, reg_log, reglog, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('reglog/', reglog, name='reglog'),
    path('api/reg_log/', reg_log),
    path('about_us/', about_us, name='about_us'),
    path('api/get_jwt_token_from_cookie/', get_jwt_token_from_cookie),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    path('api/file/', get_file),
    path('api/file_name/', get_file_name),
]