from users.views import decode_jwt  # Импорт функции декодирования токена

def user_context(request):
    if request.COOKIES.get('access_token'):
        token = request.COOKIES.get('access_token')
        decoded_result = decode_jwt(token)
        if decoded_result['valid']:
            return {'username': decoded_result['name']}
    return {'username': 'Войти'}
