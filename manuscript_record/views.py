import json
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_authent.token_authentication import TokenAuthenticationRedis
from user_authent.views import recode_operation_log
from periodical_management_system.settings import VIEW_OUT_TIME
from .celery_task import selectSubjectOrTradeOrContributionTypeTask, createSubjectOrTradeOrContributionTypeTask, \
    updateSubjectOrTradeOrContributionTypeTask


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class SubjectView(APIView):
    """
    研究方向处理视图
    """
    # authentication_classes = []
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        获取研究方向
        :param request:
        :return:
        """
        selectSubjectTaskResult = json.loads(selectSubjectOrTradeOrContributionTypeTask.delay(options='subject').get())
        return Response(status=200, data={"data": selectSubjectTaskResult['data']})

    @recode_operation_log(operation="user create new subject", level='warning')
    def post(self, request) -> Response:
        """
        创建研究方向
        :param request:
        :return:
        """
        if request.user.has_perm("manuscript_record.add_trademodel"):
            newSubjectData = request.data.copy()
            newSubjectData['options'] = 'subject'
            createSubjectTaskResult = json.loads(
                createSubjectOrTradeOrContributionTypeTask.delay(**newSubjectData).get())
            return Response(status=createSubjectTaskResult['status'], data={'message': createSubjectTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    @recode_operation_log(operation="user modify subject", level='warning')
    def put(self, request) -> Response:
        """
        修改研究方向信息
        :param request:
        :return:
        """
        if request.user.has_perm("manuscript_record.change_trademodel"):
            updateData=request.data.copy()
            updateData['options']='subject'
            updateSubjectTaskResult=json.loads(updateSubjectOrTradeOrContributionTypeTask.delay(**updateData).get())
            return Response(status=updateSubjectTaskResult['status'],data={'message':updateSubjectTaskResult['data']})
        return Response(status=200)

    def delete(self, request) -> Response:
        """
        删除研究方向
        :param request:
        :return:
        """
        return Response(status=200)

# class ManuscriptView(APIView):
#     """
#     稿件的投递，修改以及删除
#     """
#     authentication_classes=[TokenAuthenticationRedis]
#     permission_classes = [IsAuthenticated]
