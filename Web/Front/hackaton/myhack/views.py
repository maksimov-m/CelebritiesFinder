from django.shortcuts import render
from .models import AnonUser
from django.utils.crypto import get_random_string
import requests

# Главная страница с созданием уникального идентификатором сессии
def my_view(request):
    if not request.session.get('user_id'):
        user_id = get_random_string(length=10)
        request.session['user_id'] = user_id
        if not AnonUser.objects.filter(user_id=user_id).exists():
            print('2', user_id)
            AnonUser.objects.create(user_id=user_id)
    else:
        user_id = request.session['user_id']
    return render(request, 'index.html', {'user_id': user_id})



# Функция для загрузки фотографии на сервер, а также сохранение уникального номера сессии
def upload_image(request):
    if request.method == 'POST':
        file = request.FILES['file']
        url = 'http://26.221.175.97:5116/api/sendPhoto'
        files = {'file': file}
        response = requests.post(url, files=files)
        if response.ok:
            ses_id = response.text.strip('"')
            user_id = request.session.get('user_id')
            user, created = AnonUser.objects.get_or_create(user_id=user_id)
            user.server_id = ses_id
            user.save()
            return render(request, 'load.html', {'ses_id': ses_id})
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')
