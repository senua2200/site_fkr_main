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
from urllib.parse import quote, unquote
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# import datetime
from datetime import datetime, timedelta

from users.models import UploadedDocument, User, UserQuestions

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

# def index(request):
#     return render(request, 'users/index.html')
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

def reglog(request):
    return render(request, 'users/reglog.html')

def about_us(request):
    return render(request, 'users/about_us.html')
    
@sync_to_async
def check_acc(emailOrPhone, password):
    if User.objects.filter(email=emailOrPhone, password=password).exists() or User.objects.filter(phone=emailOrPhone, password=password).exists():
        return True
    else:
        return False

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'

@csrf_exempt
async def reg_log(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('maill') if data.get('maill') else data.get('emailOrPhone', '')
        password = data.get('password', '')
        check_acc_value = await check_acc(email, password)

        if data.get('name') == None or data.get('tel') == None:
            if check_acc_value!=True: 
                print("Такого пользователя не существует!!!")
                return JsonResponse({'message': "Такого пользователя не существует, нужно зарегистрироваться!"})
            else:
                print("Такой пользователь существует!!!")
                user_name_tel = await sync_to_async(lambda: User.objects.filter(email=email).first())()
                if not user_name_tel:
                    user_name_tel = await sync_to_async(lambda: User.objects.filter(phone=email).first())()
                name = user_name_tel.name
                tel = user_name_tel.phone
                email_fix = user_name_tel.email

                print(f"Создание access_token и refresh_token для email: {email_fix}, name: {name}")
                access_token = create_jwt(email_fix, name)
                print(f"Созданный access_token: {access_token}")
                refresh_token = create_refresh_token(email_fix, name)
                print(f"Созданный refresh_token: {access_token}")

                response_data = {
                    'tel2': tel,
                    'maill2': email_fix,
                    'name2': name,
                    'password2': password,
                    'check_acc_value': check_acc_value
                }
                
                response = JsonResponse(response_data)
                response = set_tokens_in_response(response, access_token, refresh_token)
                return response
            
        elif data.get('name') != None and data.get('tel') != None and check_acc_value != True:
            name = data.get('name')
            tel = data.get('tel')
            user_exists = await sync_to_async(lambda: User.objects.filter(email=email).exists() or User.objects.filter(phone=tel).exists())()
            if user_exists:
                return JsonResponse({'message': 'Такой пользователь уже зарегистрирован, попробуйте другую почту или номер телефона'})
            print("Такого пользователя не существует, но сейчас мы его создадим!!!")
            user = User(name=name, email=email, phone=tel, password=password)
            await sync_to_async(user.save)()
            await send_confirmation_email(user)
            print(f"Создание access_token и refresh_token для email: {email}, name: {name}")
            access_token = create_jwt(email, name)
            print(f"Созданный access_token: {access_token}")
            refresh_token = create_refresh_token(email, name)
            print(f"Созданный refresh_token: {access_token}")

            response_data = {
                'tel2': tel,
                'maill2': email,
                'name2': name,
                'password2': password,
                'check_acc_value': check_acc_value  # Здесь все должно быть правильно
            }
            
            response = JsonResponse(response_data)
            response = set_tokens_in_response(response, access_token, refresh_token)
            return response
        elif check_acc_value == True:
            return JsonResponse({'message': "Такой пользователь уже зарегистрирован, попробуйте использовать другую почту или номер телефона"})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
async def get_user_question(request):
    if request.method == 'POST':
        user_questions = ''
        user_obj = ''
        user_email = ''
        data = json.loads(request.body)
        question_text = data.get('question', '')
        token = request.COOKIES.get('access_token') or request.COOKIES.get('refresh_token')
        if token:
            result = await decode_jwt(token)
            if result.get('valid'):
                user_email_or_phone = result.get('identifier', '')

                user_obj = await sync_to_async(lambda: (
                    User.objects.filter(email=user_email_or_phone).first() or
                    User.objects.filter(phone=user_email_or_phone).first()
                ))()

                user_questions = UserQuestions(question=question_text, user=user_obj)
        else:
            print("Токен невалиден или его нет")
            user_questions = UserQuestions(question=question_text)

        await sync_to_async(user_questions.save)()
        return JsonResponse({'message': "Ваш вопрос сохранен"})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
async def get_history(request):
    if request.method == 'GET':
        user_obj = ''
        token = request.COOKIES.get('access_token') or request.COOKIES.get('refresh_token')
        if token:
            result = await decode_jwt(token)
            if result.get('valid'):
                user_email_or_phone = result.get('identifier', '')

                user_obj = await sync_to_async(lambda: (
                    User.objects.filter(email=user_email_or_phone).first() or
                    User.objects.filter(phone=user_email_or_phone).first()
                ))()
                
                documents = await sync_to_async(list)(
                    UploadedDocument.objects.filter(user_id=user_obj.id)
                )

                data = [
                    {
                        'id': doc.id,
                        'file_path': doc.file_path,
                    }
                    for doc in documents
                ]

                return JsonResponse(data, safe=False)

        else:
            print("Токен невалиден или его нет")
            return JsonResponse({'error': 'Пользователь неавторизован'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
async def download_by_path(request):
    if request.method == 'GET':
        file_path = request.GET.get('file_path')
        if not file_path:
            return JsonResponse({'error': 'Отсутствует путь к файлу'}, status=400)

        decoded_path = unquote(file_path)
        full_path = os.path.join(settings.MEDIA_ROOT, decoded_path)

        file_exists = await sync_to_async(os.path.exists)(full_path)

        if file_exists:
            try:
                file = await sync_to_async(open)(full_path, 'rb')
                response = FileResponse(file, as_attachment=True, filename=os.path.basename(full_path))
                return response
            except Exception as e:
                return JsonResponse({'error': f'Ошибка при открытии файла: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'Файл не найден'}, status=404)

    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


@csrf_exempt
async def set_user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = request.COOKIES.get('access_token') or request.COOKIES.get('refresh_token')
        if token:
            result = await decode_jwt(token)
            if result.get('valid'):
                user_email_or_phone = result.get('identifier', '')

                user_obj = await sync_to_async(lambda: (
                    User.objects.filter(email=user_email_or_phone).first() or
                    User.objects.filter(phone=user_email_or_phone).first()
                ))()

                user_name = data.get('name', '')
                user_email = data.get('email', '')
                user_number = data.get('phone', '')
                user_password = data.get('password', '')

                if user_name:
                    user_obj.name = user_name
                if user_email:
                    user_obj.email = user_email
                if user_number:
                    user_obj.phone = user_number
                if user_password:
                    user_obj.password = user_password
                await sync_to_async(user_obj.save)()
                
                return JsonResponse({'message': 'Данные пользователя изменены'}, status=200)
        return JsonResponse({'error': 'Токен недействителен'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
        

@csrf_exempt
async def get_user_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        user_obj = ''
        token = request.COOKIES.get('access_token') or request.COOKIES.get('refresh_token')
        if token:
            result = await decode_jwt(token)
            if result.get('valid'):
                user_email_or_phone = result.get('identifier', '')

                user_obj = await sync_to_async(lambda: (
                    User.objects.filter(email=user_email_or_phone).first() or
                    User.objects.filter(phone=user_email_or_phone).first()
                ))()

                user_id = user_obj.id
                uploaded_file = request.FILES['file']
                # file_path = f"{user_id}_{uploaded_file.name}"
                # await sync_to_async(UploadedDocument.objects.create)(user=user_obj, file_path=file_path)

                def save_file():
                    return default_storage.save(f"uploads/{user_obj.id}/{uploaded_file.name}", ContentFile(uploaded_file.read()))
                
                file_path = await sync_to_async(save_file)()

                await sync_to_async(UploadedDocument.objects.create)(user=user_obj, file_path=file_path)

                return JsonResponse({'message': 'Файл загружен!', 'file_path': file_path})
        else:
            print("Токен невалиден или его нет")
            return JsonResponse({'error': 'Файл не получен, так как вы не авторизованы'}, status=400)
        
    return JsonResponse({'error': 'Файл не получен'}, status=400)


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

async def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_email = payload.get('email')
        user_name = payload.get('name')
        print(user_email)
        print(user_name)
        dff = ''
        user_exists = await sync_to_async(User.objects.filter(email=user_email).exists)()
        if user_exists:
            dff = await sync_to_async(User.objects.get)(email=user_email)
        if not user_exists:
            user_exists = await sync_to_async(User.objects.filter(phone=user_email).exists)()
            dff = await sync_to_async(User.objects.get)(phone=user_email)
        if dff:
            print(dff.name)
            return {
                'valid': True,
                'identifier': user_email,
                'name': user_name
            }
        return {'valid': False, 'error': 'User does not exist'}
    except JWTError as e:
        # return JsonResponse({'error': 'Invalid token', 'details': str(e), 'valid': False,}, status=401)
        print('error: Invalid token', str(e))
        return {'valid': False, 'error': 'Invalid token', 'details': str(e)}


@csrf_exempt
async def get_jwt_token_from_cookie(request):
    token=''
    if request.COOKIES.get('access_token'):
        token = request.COOKIES.get('access_token')
        result = await decode_jwt(token)
        print(result)
        if result.get('valid'):
            user_name = result.get('name')
            print(user_name)
            response = JsonResponse({'user_name': user_name})
            return response
        else:
            print("Токен невалиден или пользователь не существует")
            return JsonResponse({'error': 'Токен невалиден или пользователь не существует'}, status=401)


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