from django.test import override_settings
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings


class UserTest(APITestCase):

    apiclient = APIClient()

    def setUp(self) -> None:
        settings.CELERY_TASK_ALWAYS_EAGER=True
        User.objects.create_user(username='xuhao', password='2016', email='xuhao@foxmail.com')
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_login(self):
        rightData = {'username': 'xuhao', 'password': '2016'}
        response = self.apiclient.post('/user/login', data=rightData, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_register(self):
        data={'username':"wangmin",'password':'2016','email':"xuhao@foxmail.com"}
        response=self.apiclient.post('/user/register',data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_userInformation(self):
        userLoginResponse=self.apiclient.post('/user/login',data={'username':'xuhao','password':'2016'},format='json')
        self.assertEqual(userLoginResponse.status_code,status.HTTP_200_OK)
        self.apiclient.credentials(HTTP_AUTHORIZATION='Token ' + userLoginResponse.data['token'])
        userInformation=self.apiclient.get('/user/information')
        self.assertEqual(userInformation.status_code,status.HTTP_204_NO_CONTENT)
        self.assertDictEqual(userInformation.data,{'message':'用户未完善个人信息。'})


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def testUser(self):
        pass
