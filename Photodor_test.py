# test_api.py
import requests
import tempfile

BASE_URL = "http://localhost:8000"


def test_upload_photo():
    url = f"{BASE_URL}/append"
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(b"fake_image_content")
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        files = {"photo": f}
        response = requests.post(url, files=files)

    assert response.status_code == 200


def test_get_photos():
    url = f"{BASE_URL}/reception"
    response = requests.get(url)
    assert response.status_code == 200


def test_delete_photo():
    session = requests.Session()
    session.get('http://localhost:8000/delete/')

    response = session.post(
        'http://localhost:8000/delete/',
        data={'photo_id': 1}
    )
    assert response.status_code == 200