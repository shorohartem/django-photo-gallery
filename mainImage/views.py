from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Photo
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def new_page(request):
    return render(request, 'new_page.html')

@csrf_exempt
def append(request):
    error = None
    success = None

    if request.method == "POST" and request.FILES.get('photo'):
        photo_file = request.FILES.get('photo')
        photo_file.seek(0)

        try:
            img = Image.open(photo_file)
            img.verify()

            img_format = img.format

            photo_file.seek(0)
            if img_format not in ['JPEG', 'PNG']:
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
        return redirect('append')
    return render(request, 'append.html')

@csrf_exempt
def delete(request):
    if request.method == "POST":
        photo_id = request.POST.get('photo_id')
        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id)
                photo.image.delete()
                photo.delete()
                messages.success(request,f"Фото {photo_id} успешно удалено")

                print("successfully deleted", photo_id)
            except Photo.DoesNotExist:
                messages.error(request, f' Фото {photo_id} не найдено!')
        else:
            messages.error(request, 'Введите ID фото!')
    return render(request, 'delete.html')


def reception(request):
    photo_id = request.GET.get('id')

    if photo_id:
        try:
            photo = Photo.objects.get(id=photo_id)
            return render(request, 'reception.html', {'photo': photo})
        except Photo.DoesNotExist:
            messages.error(request, f'Нет фото с ID: {photo_id}')
            photos = Photo.objects.all().order_by('-id')
            return render(request, 'reception.html', {'photos': photos})

    photos = Photo.objects.all().order_by('-id')
    return render(request, 'reception.html', {'photos': photos})

def reception_all(request):
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'all_photos.html', {'photos': photos})

def all_photo(request):
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'all_photo.html', {'photos': photos})
