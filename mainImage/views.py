from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Photo
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PhotoSerializer
import time


logger = logging.getLogger(__name__)


def log_request(request, response=None, extra=None):
    user = request.user.id if request.user.is_authenticated else "Anonymous"
    duration = time.time() - request.start_time if hasattr(request, 'start_time') else 0

    log_data = {
        'method': request.method,
        'path': request.get_full_path(),
        'ip': request.META.get('REMOTE_ADDR'),
        'user': user,
        'status': response.status_code if response else '???',
        'duration': f"{duration:.3f}s"
    }

    if extra:
        log_data.update(extra)

    log_str = f"[{request.method}] {request.path} | IP: {log_data['ip']} | User: {user} | Status: {log_data['status']} | Time: {log_data['duration']}"
    if extra:
        log_str += f" | {extra}"

    logger.info(log_str)

def new_page(request):
    return render(request, 'new_page.html')

@csrf_exempt
def append(request):
    request.start_time = time.time()

    if request.method == "POST" and request.FILES.get('photo'):
        photo_file = request.FILES.get('photo')
        photo_file.seek(0)
        logger.info(f"Добавление фото: {photo_file.name} ")

        try:
            img = Image.open(photo_file)
            img.verify()

            img_format = img.format
            logger.info(f"Формат фото: {img_format}")

            photo_file.seek(0)
            if img_format not in ['JPEG', 'PNG']:
                logger.info(f"Получен неверный формат [{img_format}]")
                messages.error(request, 'Неправильный формат фото!!!')
                return redirect('append')

        except Exception:
            messages.error(request, 'Неправильный формат фото!!!')
            return redirect('append')

        title = photo_file.name.rsplit('.', 1)[0]

        Photo.objects.create(
            title=title,
            image=photo_file
        )
        messages.success(request, 'Фото добавлено!')
        logger.info(f'Фото {title} добавлено!')
        return redirect('append')
    response = render(request, 'append.html')
    log_request(request, response=response)
    return render(request, 'append.html')

@csrf_exempt
def delete(request):

    request.start_time = time.time()

    if request.method == "POST":
        photo_id = request.POST.get('photo_id')
        logger.info(f'Запрошено удаление фото: {photo_id}')
        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id)
                photo.image.delete()
                photo.delete()
                messages.success(request,f"Фото {photo_id} успешно удалено")
                logger.info(f"Фото: {photo_id} удалено")
                print("successfully deleted", photo_id)

            except Photo.DoesNotExist:
                messages.error(request, f' Фото {photo_id} не найдено!')
                logger.info(f'Не найдено фото:{photo_id}')
        else:
            messages.error(request, 'Введите ID фото!')

    response = render(request, 'delete.html')
    log_request(request, response=response)
    return render(request, 'delete.html')


def reception(request):
    request.start_time = time.time()

    photo_id = request.GET.get('id')
    logger.info(f" Запрос на получение фото: {photo_id}")

    if photo_id:
        try:
            photo = Photo.objects.get(id=photo_id)
            logger.info(f"Фото получено: {photo_id}")
            return render(request, 'reception.html', {'photo': photo})


        except Photo.DoesNotExist:
            messages.error(request, f'Нет фото с ID: {photo_id}')
            photos = Photo.objects.all().order_by('-id')
            logger.info(f"Нет фото с таким ID: {photo_id}")
            return render(request, 'reception.html', {'photos': photos})

    photos = Photo.objects.all().order_by('-id')
    response = render(request, 'reception.html')
    log_request(request, response=response)
    return render(request, 'reception.html', {'photos': photos})


def all_photo(request):
    request.start_time = time.time()

    photos = Photo.objects.all().order_by('-id')
    logger.info("Получение всех фотографий")
    response = render(request, 'all_photo.html')
    log_request(request, response=response)
    return render(request, 'all_photo.html', {'photos': photos})

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
