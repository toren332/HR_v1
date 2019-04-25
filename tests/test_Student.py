import pytest

from django.contrib.auth.models import User
from profiles import models

# TODO: https://www.python.org/dev/peps/pep-0008/
# https://www.python.org/dev/peps/pep-0008/#descriptive-naming-styles
# test_Account.py -> test_account.py

# TODO: install flask8 and run it
# TODO: install pep8 and run it

from django.urls import reverse

from rest_framework.test import APIClient

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def student_of_ivan():
    user = User.objects.create_user(username='ivan', email='ivan@test.test', password='xa6eiQuoo3')
    profile = models.Profile.objects.get(user=user)
    profile.kind = 'student'
    profile.save()
    student = models.Student.objects.create(profile=profile)
    return student


@pytest.fixture
def client():
    return APIClient()


# noinspection PyMethodMayBeStatic
class EnterGroupTest:
    def test_201(self, student_of_ivan, client):
        # Ivan enter group
        group = models.Group.objects.create(name='Group12')

        # WHAT?! student_of_ivan.profile.user.id == student_of_ivan.id
        # coz your Profile.id == User.id, isn't it?
        student_id = student_of_ivan.profile.user.id

        data = {
            'group': group.id,
        }
        # https://realpython.com/python-string-formatting/#3-string-interpolation-f-strings-python-36
        url = '/api_v1/students/'+str(student_id)+'/enter_group/'
        response = client.post(url, data=data)

        assert response.status_code == 201
        assert response.data
        return {'group_id': group.id, 'student_id': student_id}

    def test_400_1(self, client):
        # anonymous user enter group
        group = models.Group.objects.create(name='Group12')
        data = {
            'group': group.id,
        }
        url = '/api_v1/students/'+str(1)+'/enter_group/'
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data

    def test_400_2(self,student_of_ivan, client):
        # Ivan enter empty group
        student_id = student_of_ivan.profile.user.id

        data = {
            'group': 1,
        }
        url = '/api_v1/students/'+str(student_id)+'/enter_group/'
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data


class ExitGroupTest:
    def test_200(self, student_of_ivan, client):
        # Ivan exit entered group
        _ = EnterGroupTest.test_201(EnterGroupTest(), student_of_ivan=student_of_ivan, client=client)
        data = {
            'group': _['group_id'],
        }
        url = '/api_v1/students/'+str(_['student_id'])+'/exit_group/'
        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.data

    def test_400_1(self,student_of_ivan, client):
        # Ivan exit not entered group
        _ = EnterGroupTest.test_201(EnterGroupTest(), student_of_ivan=student_of_ivan, client=client)
        data = {
            'group': _['group_id']+101,
        }
        url = '/api_v1/students/' + str(_['student_id']) + '/exit_group/'
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data

    def test_400_2(self, client):
        # anonymous user exit not entered group
        group = models.Group.objects.create(name='Group12')
        data = {
            'group': group.id,
        }
        url = '/api_v1/students/' + str(1) + '/exit_group/'
        response = client.post(url, data=data)

        assert response.status_code == 400
        assert response.data