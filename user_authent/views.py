# -*- coding: utf-8 -*-
# Generated by xuhao on 2020/11/18 11:23

import json
import logging
from enum import Enum, unique
from django.contrib.auth.hashers import make_password
from periodical_management_system.settings import TOKEN_OUT_TIME, VIEW_OUT_TIME
from django.core import signing
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView

from .models import UserMenuModel
from .token_authentication import TokenAuthenticationRedis
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .modelSerializer import UserMenuModelSerialzier
from django.utils.decorators import method_decorator
from .celery_task import userRegister, sendIdentityCode, selectUserInformation, modifyUserInformation, \
    createUserInformation, getUserMenuTask, createUserMenuTask, deleteUserMenuTask, modifyUserMenuTask

redis_connection = get_redis_connection()


@unique
class LogLevelEnum(Enum):
    """
    系统日志等级
    """
    INFO = 'info'
    ERROR = 'error'
    DEBUG = 'debug'
    WARNING = 'warning'


def recode_operation_log(operation, level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == LogLevelEnum.ERROR.value:
                logging.error(operation)
            elif level == LogLevelEnum.WARNING.value:
                logging.warning(operation)
            elif level == LogLevelEnum.DEBUG.value:
                logging.debug(operation)
            else:
                logging.info(operation)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@method_decorator(csrf_exempt, name='post')
class LoginView(APIView):
    """
    用户登录视图
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = User.objects.filter(username=username)
        if user:
            authent = authenticate(username=username, password=password)
            if authent:
                if authent.is_active:
                    login(request, authent)
                    token = signing.dumps(username)
                    redis_connection.setex(username + ':token', TOKEN_OUT_TIME, token)
                    return Response(status=200, data={'token': token, 'username': username})
                else:
                    return Response(status=204, data={'message': 'Wrong password.'})
            return Response(status=204, data={"message": "Wrong user name or password."})
        else:
            return Response(status=204, data={'message': "Wrong user name or password."})


@method_decorator(csrf_exempt, name='post')
class RegisterView(APIView):
    """
    用户注册视图
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user_register_data = {'username': request.data.get('username'),
                              "password": request.data.get('password'),
                              "email": request.data.get('email')}
        register_task = userRegister.delay(**user_register_data)
        # async_task=AsyncResult(id=register_task.id,app=app)
        register_result = register_task.get()
        if register_result:
            return Response(status=200, data={'message': "注册成功！"})
        return Response(status=204)


class ChangePasswordView(APIView):
    """
    用户密码修改视图
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def put(self, request):
        username = request.data.get('username', None)
        user = User.objects.filter(username=username).first()
        if user and user.email:
            identityCode = redis_connection.get(username + ":identity")
            if identityCode:
                userInputPassword = request.data.get('password', None)
                userInputIdentityCode = request.data.get('identityCode', None)
                if userInputPassword and userInputIdentityCode:
                    user.password = make_password(userInputPassword, None, 'pbkdf2_sha256')
                    user.save()
                    return Response(status=200, data={"message": "密码修改成功！"})
                return Response(status=204, data={"message": "密码修改失败！"})
            else:
                sendIdentityCodeResult = json.loads(sendIdentityCode.delay(username).get())
                if sendIdentityCodeResult['result'] == 'success':
                    return Response(status=200, data={"message": sendIdentityCodeResult['message']})
                else:
                    return Response(status=204, data={"message": sendIdentityCodeResult['message']})
        return Response(status=204, data={"message": "用户不存在或者用户未绑定个人邮箱！"})


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class UserInformationView(APIView):
    """用户个人信息维护视图"""
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = str(request.user)
        selectUserInformationResult = json.loads(selectUserInformation.delay(username).get())
        if 'result' in selectUserInformationResult.keys():
            return Response(status=204, data={'message': selectUserInformationResult['message']})
        return Response(status=200, data=selectUserInformationResult)

    @recode_operation_log("Users modify their personal information.", 'info')
    def put(self, request):
        username = str(request.user)
        userInputInformation = request.data
        modifyUserInformationResult = json.loads(modifyUserInformation.delay(username, **userInputInformation).get())
        if modifyUserInformationResult['result'] == 'success':
            return Response(status=200, data={'message': modifyUserInformationResult['message']})
        else:
            if 'error' in modifyUserInformationResult.keys():
                return Response(status=204, data={'message': modifyUserInformationResult['message'],
                                                  'error': modifyUserInformationResult['error']})
            else:
                return Response(status=204, data={"message": modifyUserInformationResult['message']})

    @recode_operation_log("Users create personal information records.", 'info')
    def post(self, request):
        username = request.user.__str__()
        userInputInformation = request.data
        createUserInformationResult = json.loads(createUserInformation.delay(username, **userInputInformation).get())
        if createUserInformationResult['result'] == 'success':
            return Response(status=200, data={"message": createUserInformationResult['message']})
        else:
            return Response(status=204, data={'message': createUserInformationResult['message']})


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class MenuView(APIView):
    """
    用户菜单获取处理视图
    """
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        根据用户所属用户组查询用户菜单
        :param request:
        :return:
        """
        menuList = json.loads(getUserMenuTask.delay(user=request.user.id, username=request.user.__str__()).get())
        return Response(status=200, data={"message": menuList})

    @recode_operation_log('user create menu.', 'warning')
    def post(self, request) -> Response:
        """
        创建用户菜单，后继会加入权限要求。
        :param request:
        :return:
        """
        menuData = request.data
        createUserMenuResult = json.loads(createUserMenuTask.delay(**menuData).get())
        if createUserMenuResult['result'] == 'success':
            return Response(status=200, data={'message': createUserMenuResult['message']})
        return Response(status=204, data={'message': createUserMenuResult['message']})

    def delete(self, request) -> Response:
        """
        如用户具有删除菜单权限，即可删除菜单，后端返回的菜单查询中将不含该删除菜单。
        如果删除的是一级菜单，则其子菜单将一并删除，而删除子菜单，则不影响父菜单
        :param request:
        :return:
        """
        if request.user.has_perm('user_authent.delete_usermenumodel'):
            options = request.data.get('options', None)
            delete_menu_role=request.data.get('menu_role',None)
            if not options and not delete_menu_role:
                return Response(status=204,data={"message":"数据格式不正确！"})
            # deleteUserMenuTaskResult=json.loads(deleteUserMenuTask(options))
            deleteUserMenuTaskResult = json.loads(deleteUserMenuTask.delay(options,delete_menu_role).get())
            return Response(status=deleteUserMenuTaskResult['status'],
                            data={"message": deleteUserMenuTaskResult['data']})
        return Response(status=204, data={"message": '无相应权限。'})

    def put(self, request) -> Response:
        """
        修改菜单信息
        :param request:
        :return:
        """
        if request.user.has_perm('user_authent.change_usermenumodel'):
            new_menu_data = request.data
            modifyUserMenuTaskResult = json.loads(modifyUserMenuTask.delay(**new_menu_data).get())
            return Response(status=modifyUserMenuTaskResult['status'],
                            data={'message': modifyUserMenuTaskResult['data']})
        return Response(status=204, data={"message": "无相应权限。"})
