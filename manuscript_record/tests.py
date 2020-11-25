import time
import json
from django.conf import settings
from django.contrib.auth.models import User,Group,Permission
from rest_framework.test import APIClient,APITestCase
from .models import SubjectModel
from datetime import datetime
from rest_framework import status

class TestSubject(APITestCase):

    client=APIClient()

    def setUp(self) -> None:
        settings.CELERY_TASK_ALWAYS_EAGER=True
        superuser=User.objects.create_superuser(username='xuhao',email='xuhao2018@foxmail.com',password='2016')
        administrators=Group.objects.create(name="administrators")
        allPermission=Permission.objects.all()
        permissionlist=[item.id for item in allPermission]
        administrators.permissions.set(permissionlist)
        for item in range(10):
            currentTime=datetime.now()
            id = 'S'+str(currentTime.year) + str(currentTime.month) + str(currentTime.day) + \
                 str(currentTime.hour) + str(currentTime.minute) + str(currentTime.second)
            time.sleep(1)
            SubjectModel.objects.create(id=id,name="测试"+str(item),brief_introduction="测试"+str(item)+"简介")
        superuser.groups.add(administrators)
        userlogin = self.client.post('/user/login', data=dict(username='xuhao', password='2016'), format='json')
        self.assertEqual(status.HTTP_200_OK, userlogin.status_code)
        token = json.loads(userlogin.content.decode('utf-8'))['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


    def test_selectSubject(self):
        selectSubject=self.client.get('/record/subject')
        self.assertEqual(selectSubject.status_code,status.HTTP_200_OK)


    def test_createSubject(self):
        newSubjectData={'name':'测试13','brief_introduction':"测试二简介"}
        createSubject=self.client.post('/record/subject',data=newSubjectData,format='json')
        self.assertEqual(status.HTTP_200_OK,createSubject.status_code)




