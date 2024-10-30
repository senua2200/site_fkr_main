from email.policy import strict
import json
import os
import time
import asyncio
import threading
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse, JsonResponse
from urllib.parse import quote
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# import datetime
from datetime import datetime, timedelta

from users.models import User

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from jose import JWTError, jwt

from django.contrib.auth.tokens import PasswordResetTokenGenerator

def index(request):
    """ if request.COOKIES.get('access_token'):
        token = request.COOKIES.get('access_token')
        decoded_result = decode_jwt(token)
        if decoded_result['valid']:
            context={'username': decoded_result['name']}
        else:
            context={'username': 'Войти'}
    else:
        context={'username': 'Войти'}
    return render(request, 'users/index.html', context) """
    return render(request, 'users/index.html')

def reglog(request):
    return render(request, 'users/reglog.html')

def about_us(request):
    return render(request, 'users/about_us.html')
    
@sync_to_async
def check_acc(email, number):
    return User.objects.filter(email=email, number=number).exists()

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'

@csrf_exempt
async def reg_log(request):
    if request.method == 'POST':
        print("это должно быть 1")
        data = json.loads(request.body)
        number = data.get('tel', '')
        email = data.get('maill', '')

        check_acc_value = await check_acc(email, number)

        if check_acc_value!=True and data.get('name') == None and data.get('password') == None:
            print("Такого пользователя не существует!!!")
            # return JsonResponse({'error': 'User already exists'}, status=400)
            return JsonResponse({'message': "Такого пользователя не существует, нужно зарегистрироваться!"})
        if check_acc_value:
            print("Такой пользователь существует!!!")
            user_name_password = await sync_to_async(lambda: User.objects.filter(email=email).first())()
            name = user_name_password.name
            password = user_name_password.password
            print('ИМЯ ИМЯ ИМЯ ИМЯ')
            print(name)
            print(password)

            print(f"Создание access_token и refresh_token для email: {email}, name: {name}")
            access_token = create_jwt(email, name)
            print(f"Созданный access_token: {access_token}")
            refresh_token = create_refresh_token(email, name)
            print(f"Созданный refresh_token: {access_token}")

            response_data = {
                'tel2': number,
                'maill2': email,
                'name2': name,
                'password2': password,
                'check_acc_value': check_acc_value  # Здесь все должно быть правильно
            }
            
            response = JsonResponse(response_data)
            response = set_tokens_in_response(response, access_token, refresh_token)
            return response
            """ НУЖНО СОБРАТЬ RESPONSE ПО ДРУГОМУ - С УЧЕТОМ ТОКЕНОВ """
            return JsonResponse({'email': email, 'number': number, 'check_acc_value': check_acc_value})
        if check_acc_value!=True and data.get('name') and data.get('password'):
            print("Такого пользователя не существует, но сейчас мы его создадим!!!")
            # return JsonResponse({'error': 'User already exists'}, status=400)


        if data.get('name') and data.get('password'):
            name = data.get('name')
            password = data.get('password')
            print("это должно быть 2")
            user = User(name=name, email=email, number=number, password=password)
            await sync_to_async(user.save)()  # Сохраняем пользователя асинхронно
            print("это должно быть 3")
            await send_confirmation_email(user)
            print(f"Создание access_token и refresh_token для email: {email}, name: {name}")
            access_token = create_jwt(email, name)
            print(f"Созданный access_token: {access_token}")
            refresh_token = create_refresh_token(email, name)
            print(f"Созданный refresh_token: {access_token}")

            # Убедитесь, что здесь не возникает корутины
            response_data = {
                'tel2': number,
                'maill2': email,
                'name2': name,
                'password2': password,
                'check_acc_value': check_acc_value  # Здесь все должно быть правильно
            }
            
            response = JsonResponse(response_data)
            response = set_tokens_in_response(response, access_token, refresh_token)
            return response
        """ else:
            if check_acc_value:
                print("Пользователь существует")
                response_data = {
                    'tel2': number,
                    'maill2': email,
                    'check_acc_value': check_acc_value  # Здесь все должно быть правильно
                }
                response = JsonResponse(response_data)
                return response
                # return JsonResponse({'message': "gooood"})
            if check_acc_value!=True:
                print("Пользователя нет")
                return JsonResponse({'error': 'User already exists'}, status=400) """

    return JsonResponse({'error': 'Invalid request'}, status=400)

def set_tokens_in_response(response, access_token, refresh_token):
    response.set_cookie('access_token', access_token, max_age=3600, httponly=False)
    response.set_cookie('refresh_token', refresh_token, max_age=36000, httponly=False)
    return response

def create_jwt(email3, name):
    payload = {
        'email': email3,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(email3, name):
    payload = {
        'email': email3,
        'name': name,
        'exp': datetime.utcnow() + timedelta(days=30),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_email = payload.get('email')
        user_name = payload.get('name')
        print(user_email)
        print(user_name)
        if User.objects.filter(email=user_email).exists():
            dff = User.objects.get(email=user_email)
            print(dff.name)
            return {
                'valid': True,
                'email': user_email,
                'name': user_name
            }
        return {'valid': False, 'error': 'User does not exist'}
    except JWTError as e:
        return JsonResponse({'error': 'Invalid token', 'details': str(e), 'valid': False,}, status=401)
    

@csrf_exempt
def get_jwt_token_from_cookie(request):
    token=''
    if request.COOKIES.get('access_token'):
        token = request.COOKIES.get('access_token')
        print(decode_jwt(token))
    else:
        ref_token = request.COOKIES.get('refresh_token')
        if not ref_token:
            return JsonResponse({'error': 'Полный пиздец'}, status=401)
        else:
            print("Рефреш есть")
            try:
                payload = jwt.decode(ref_token, SECRET_KEY, algorithms=[ALGORITHM])
                print('добавляю почту в новые токены')
                user_email = payload.get('email')
                user_name = payload.get('name')
                access_token = create_jwt(user_email, user_name)
                refresh_token = create_refresh_token(user_email, user_name)            

                response = JsonResponse({'message': "new token go"})
                # Установка куки с JWT и Refresh токеном
                response.set_cookie(
                    'access_token',
                    access_token,
                    max_age=3600,  # 1 час
                    httponly=False,  # Только для HTTP
                    secure=False,  # False, так как используем HTTP (на проде нужно ставить True при использовании HTTPS)
                    samesite=None,  # Разрешаем отправку с разных источников
                )
                response.set_cookie(
                    'refresh_token', 
                    refresh_token, 
                    max_age=36000,  # 10 часов
                    httponly=False,  # Только для HTTP
                    secure=False,  # False, так как используем HTTP (на проде нужно ставить True при использовании HTTPS)
                    samesite=None,  # Разрешаем отправку с разных источников
                )

                return response
            except JWTError as e:
                return JsonResponse({'error': 'Invalid refresh token', 'details': str(e)}, status=401)

    return JsonResponse({'message': 'Token is valid', 'user': token})




class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Используй другие атрибуты пользователя, которые точно есть, например, pk и is_active
        return f"{user.pk}{timestamp}{user.is_active}"

custom_token_generator = CustomTokenGenerator()

async def send_confirmation_email(user):
    token = custom_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    print(f"Token: {token}, UID: {uid}")
    print(f"PK: {user.pk}" )
    uid1 = urlsafe_base64_decode(uid).decode()
    print(uid1)
    activation_link = f"http://localhost:8000/activate/{uid}/{token}/"
    """ activation_link = f"https://bec1-80-83-235-78.ngrok-free.app/activate/{uid}/{token}/" """
    print(f"Отправка письма на: {user.email}")

    mail_subject = 'Подтверждение вашей регистрации'
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })
    send_mail(mail_subject, message, 'lol20033002lol@gmail.com', [user.email])
    print('Все окей')
    check_thread = threading.Thread(target=start_check_date, args=(user.email, datetime.now()))
    check_thread.start()

def start_check_date(user_email, date_time):
    # Обертка для асинхронного вызова check_date в фоне
    asyncio.run(check_date(user_email, date_time))



def activate_account(request, uidb64, token):
    print("ОПП")
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    print(f"UID: {uid}")
    print(f"User: {user}")
    print(f"Received Token: {token}")
    print(f"Generated Token: {custom_token_generator.make_token(user)}")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(f"UID: {uid}")
        print(f"User: {user}")
        print(f"Received Token: {token}")
        print(f"Generated Token: {custom_token_generator.make_token(user)}")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and custom_token_generator.check_token(user, token):
        print('мы дошли до сюда')
        user.is_active = True
        user.save()
        print(user.is_active, " = user.is_active в бд")
        return HttpResponse('Спасибо за подтверждение email!')
    else:
        return HttpResponse('Ссылка для подтверждения недействительна!')
    
""" async def check_date(user_email, date_time):
    try:
        while True:
            print(f"Начало check_date для пользователя {user_email}")
            await asyncio.sleep(5)
            elapsed_time = datetime.now() - date_time
            print(f"Текущее время: {datetime.now()}, Время начала: {date_time}, Разница: {elapsed_time}")
            if elapsed_time >= timedelta(seconds=20):
                print(f"Пользователь {user_email} был удален за неактивность")
                break
            else:
                print("Через 5 секунд проверю регистрацию пользователя")
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}") """

async def check_date(user_email, date_time):
    try:
        while True:
            print(f"Начало check_date для пользователя {user_email}")
            user = await sync_to_async(User.objects.get)(email=user_email)
            print(user.is_active)
            if user.is_active:
                break
            else:
                await asyncio.sleep(5)
                elapsed_time = datetime.now() - date_time
                print(f"Текущее время: {datetime.now()}, Время начала: {date_time}, Разница: {elapsed_time}")
                if elapsed_time >= timedelta(seconds=60):
                    print("удалить его - "+user_email)
                    await sync_to_async(user.delete)()
                    print(f"Пользователь {user_email} был удален за неактивность")
                    break
                else:
                    print("Через 5 секунд проверю регистрацию пользователя")
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")


@csrf_exempt
def get_file_name(request):
    if request.method == 'POST' and request.FILES.get('file'):
        up_file = request.FILES['file']
        return JsonResponse({'file_name': up_file.name})
    return JsonResponse({'error': 'No name file uploaded'}, status=400)

@csrf_exempt
def get_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        up_file = request.FILES['file']
        file_name = default_storage.save(up_file.name, ContentFile(up_file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{quote(up_file.name)}"'    
        return response
    return JsonResponse({'error': 'No file uploaded'}, status=400)