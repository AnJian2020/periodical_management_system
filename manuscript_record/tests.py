import json
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from rest_framework.test import APIClient, APITestCase
from .models import SubjectModel, TradeModel, ContributionTypeModel
from datetime import datetime
from rest_framework import status


class TestSubject(APITestCase):
    client = APIClient()

    def setUp(self) -> None:
        settings.CELERY_TASK_ALWAYS_EAGER = True
        superuser = User.objects.create_superuser(username='xuhao', email='xuhao2018@foxmail.com', password='2016')
        administrators = Group.objects.create(name="administrators")
        allPermission = Permission.objects.all()
        permissionlist = [item.id for item in allPermission]
        administrators.permissions.set(permissionlist)
        for item in range(10):
            currentTime = datetime.now()
            idNumber = str(currentTime.year) + str(currentTime.month) + str(currentTime.day) + str(
                currentTime.hour) + str(currentTime.minute) + str(currentTime.second) + str(item)
            subjectID = 'S' + idNumber
            tradeID = 'T' + idNumber
            contributionTypeID = 'C' + idNumber

            SubjectModel.objects.create(id=subjectID, name="测试研究方向" + str(item),
                                        brief_introduction="测试研究方向" + str(item) + "简介")

            TradeModel.objects.create(id=tradeID, name="测试行业领域" + str(item),
                                      brief_introduction="测试行业领域" + str(item) + "简介")

            ContributionTypeModel.objects.create(id=contributionTypeID, name="测试投稿类型" + str(item),
                                                 brief_introduction="测试投稿类型" + str(item) + "简介")

        superuser.groups.add(administrators)
        userlogin = self.client.post('/user/login', data=dict(username='xuhao', password='2016'), format='json')
        self.assertEqual(status.HTTP_200_OK, userlogin.status_code)
        token = json.loads(userlogin.content.decode('utf-8'))['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_selectSubject(self):
        """
        测试查询研究方向
        :return:
        """
        selectSubject = self.client.get('/record/subject')
        self.assertEqual(selectSubject.status_code, status.HTTP_200_OK)

    def test_createSubject(self):
        """
        测试创建研究方向
        :return:
        """
        newSubjectData = {'name': '测试13', 'brief_introduction': "测试二简介"}
        createSubject = self.client.post('/record/subject', data=newSubjectData, format='json')
        self.assertEqual(status.HTTP_200_OK, createSubject.status_code)

    def test_deleteSubject(self):
        """
        测试删除研究方向
        :return:
        """
        deleteWrongSubjectResponse=self.client.delete('/record/subject',data={'id':'S201600008848'},format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST,deleteWrongSubjectResponse.status_code)

    def test_modifySubject(self):
        """
        测试修改研究方向信息
        :return:
        """
        modifyWrongSubjectResponse=self.client.put('/record/subject',data={'id':'S201600008848','name':'xuhao',
                                                                           'brief_introduction':"测试修改"},format='json')
        self.assertEqual(modifyWrongSubjectResponse.status_code,status.HTTP_204_NO_CONTENT)




