# test_api.py
import pytest
import requests
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from mainImage.models import Photo

BASE_URL = "http://localhost:8000"
client = Client()

def test_new_page(request):
    response = client.get(' ')

    assert response.status_code == 200

@pytest.mark.django_db
def test_upload_photo():
    test_image = SimpleUploadedFile(
        "test.jpg",
        b"fake_image_content",
        content_type="image/jpeg"
    )
    response = client.post('/append', {'photo': test_image})

    assert response.status_code == 302


@pytest.mark.django_db
def test_all_photo(request):
    test_image = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    client.post('/append/', {'photo': test_image})

    response = client.get('/all/')

    assert response.status_code == 200



def test_reception_with_invalid_id():
    response = client.get('/reception/?id=99999')

    assert response.status_code == 404

def test_reception_empty():
    response = client.get('/reception')
    assert response.status_code == 200
    assert 'photos' in response.context

@pytest.mark.django_db
def test_reception_with_valid_id():
    from mainImage.models import Photo
    from django.core.files.uploadedfile import SimpleUploadedFile

    test_image = SimpleUploadedFile(
        "test.jpg",
        b"fake_content",
        content_type="image/jpeg"
    )
    photo = Photo.objects.create(title="Test", image=test_image)
    response = client.get(f'/reception?id={photo.id}')

    assert response.status_code == 200

@pytest.mark.django_db
def test_reception_with_invalid_id():
    response = client.get('/reception?id=99999')

    assert response.status_code == 200


def test_append_get_request():
    response = client.get('/append')

    assert response.status_code == 200

@pytest.mark.django_db
def test_append_post_without_file():
    response = client.post('/append')

    assert response.status_code == 200
    assert Photo.objects.count() == 0

def test_get_photos():
    url = f"{BASE_URL}/reception"
    response = requests.get(url)

    assert response.status_code == 200









def test_delete_get_request():
    response = client.get('/delete/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_invalid_id():
    response = client.post('/delete/', {'photo_id': 99999})

    assert response.status_code == 200
    assert Photo.objects.count() == Photo.objects.count()
    assert 'Фото 99999 не найдено' in response.content.decode()


def test_delete_photo():
    session = requests.Session()
    session.get('http://localhost:8000/delete/')

    response = session.post(
        'http://localhost:8000/delete/',
        data={'photo_id': 1}
    )
    assert response.status_code == 200