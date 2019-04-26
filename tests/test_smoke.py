import pytest

from rest_framework.test import APIClient

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def client():
    return APIClient()


# noinspection PyMethodMayBeStatic
class UserViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/users/')
        assert resp.status_code == 200


class ProfileViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/profiles/')
        assert resp.status_code == 200


class StudentViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/students/')
        assert resp.status_code == 200


class TeacherViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/teachers/')
        assert resp.status_code == 200


class ClientViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/clients/')
        assert resp.status_code == 200


class GroupViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/groups/')
        assert resp.status_code == 200


class LessonViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/lessons/')
        assert resp.status_code == 200


class UniversityViewSetTest:
    def test_200(self, client):
        resp = client.get('http://127.0.0.1:8000/api_v1/universities/')
        assert resp.status_code == 200


class UniversityCreateTest:
    def test_200(self, client):
        data = {
            "name": "МГУ",
            "english_name": "MSU",
            "description": "asfkja'sdlkfj"
        }
        resp = client.post('http://127.0.0.1:8000/api_v1/universities/', data=data)
        assert resp.status_code == 201