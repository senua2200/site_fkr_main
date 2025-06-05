
from django.contrib import admin
from django.urls import path

from users.views import about_us, activate_account, get_file, get_file_name, get_jwt_token_from_cookie, reg_log, reglog, get_user_question, set_user_data, get_user_file, get_history, download_by_path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    path('reglog/', reglog, name='reglog'),
    path('api/reg_log/', reg_log),
    path('api/get_user_question/', get_user_question),
    path('api/set_user_data/', set_user_data),
    path('api/get_user_file/', get_user_file),
    path('api/get_history/', get_history),
    path('api/download_by_path/', download_by_path, name='download_by_path'),
    path('about_us/', about_us, name='about_us'),
    path('api/get_jwt_token_from_cookie/', get_jwt_token_from_cookie),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    path('api/file/', get_file),
    path('api/file_name/', get_file_name),
]