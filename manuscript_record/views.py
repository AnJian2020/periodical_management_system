import json
from .modelSerializer import ManuscriptModelSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_authent.token_authentication import TokenAuthenticationRedis
from user_authent.views import recode_operation_log
from periodical_management_system.settings import VIEW_OUT_TIME
from .celery_task import selectSubjectOrTradeOrContributionTypeTask, createSubjectOrTradeOrContributionTypeTask, \
    updateSubjectOrTradeOrContributionTypeTask, deleteSubjectOrTradeContributionTypeTask, deliverManuscriptTask, \
    selectUserPersonalManuscriptTask, deleteUserPersonalManuscriptTask, modifyUserPersonalManuscriptTask


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class SubjectView(APIView):
    """
    研究方向处理视图
    """
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
        if request.user.has_perm("manuscript_record.add_subjectmodel"):
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
        if request.user.has_perm("manuscript_record.change_subjectmodel"):
            updateData = request.data.copy()
            updateData['options'] = 'subject'
            updateSubjectTaskResult = json.loads(updateSubjectOrTradeOrContributionTypeTask.delay(**updateData).get())
            return Response(status=updateSubjectTaskResult['status'], data={'message': updateSubjectTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    @recode_operation_log(operation="user delete subject", level='warning')
    def delete(self, request) -> Response:
        """
        删除研究方向
        :param request:
        :return:
        """
        if request.user.has_perm('manuscript_record.delete_subjectmodel'):
            deleteSubjectId = request.data.get('id', None)
            if deleteSubjectId:
                deleteSubjectResult = json.loads(
                    deleteSubjectOrTradeContributionTypeTask.delay(options='subject', idOrName=deleteSubjectId).get())
                return Response(status=deleteSubjectResult['status'], data={"message": deleteSubjectResult['data']})
            return Response(status=404, data={"message": "缺少部分参数。"})
        return Response(status=403, data={"message": "该用户无相应权限。"})


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class TradeView(APIView):
    """
    行业领域视图
    """
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    @recode_operation_log(operation="user delete trade", level='warning')
    def delete(self, request):
        """
        删除行业领域
        :param request:
        :return:
        """
        if request.user.has_perm('manuscript_record.delete_trademodel'):
            deleteTradeId = request.data.get('id', None)
            if deleteTradeId:
                deleteTradeResult = json.dumps(
                    deleteSubjectOrTradeContributionTypeTask.delay(options='trade', idOrName=deleteTradeId).get())
                return Response(status=deleteTradeId['status'], data={"message": deleteTradeResult['data']})
            return Response(status=404, data={"message": "缺少部分参数。"})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    def get(self, request):
        """
        获取行业领域
        :param request:
        :return:
        """
        selectTradeTaskResult = json.loads(selectSubjectOrTradeOrContributionTypeTask.delay(options='trade').get())
        return Response(status=200, data={"data": selectTradeTaskResult['data']})

    @recode_operation_log(operation="user create new trade", level='warning')
    def post(self, request):
        """
        创建行业领域
        :param request:
        :return:
        """
        if request.user.has_perm("manuscript_record.add_trademodel"):
            newTradeData = request.data.copy()
            newTradeData['options'] = 'trade'
            createTradeTaskResult = json.loads(
                createSubjectOrTradeOrContributionTypeTask.delay(**newTradeData).get())
            return Response(status=createTradeTaskResult['status'], data={'message': createTradeTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    @recode_operation_log(operation="user modify trade", level='warning')
    def put(self, request):
        """
        修改行业领域信息
        :param request:
        :return:
        """
        if request.user.has_perm("manuscript_record.change_trademodel"):
            updateData = request.data.copy()
            updateData['options'] = 'trade'
            updateTradeTaskResult = json.loads(updateSubjectOrTradeOrContributionTypeTask.delay(**updateData).get())
            return Response(status=updateTradeTaskResult['status'], data={'message': updateTradeTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})


@method_decorator(cache_page(VIEW_OUT_TIME), name='get')
class ContributionTypeView(APIView):
    """
    投稿类型视图，创建、删除、获取与修改
    """
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    @recode_operation_log(operation='user create contribution type', level='warning')
    def post(self, request):
        """
        创建投稿类型
        :param request:
        :return:
        """
        if request.user.has_perm("manuscript_record.add_contributiontypemodel"):
            newTradeData = request.data.copy()
            newTradeData['options'] = 'contribution_type'
            createContributionTypeTaskResult = json.loads(
                createSubjectOrTradeOrContributionTypeTask.delay(**newTradeData).get())
            return Response(status=createContributionTypeTaskResult['status'],
                            data={'message': createContributionTypeTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    @recode_operation_log(operation="user delete contribution type.", level='warning')
    def delete(self, request):
        """
        删除投稿类型
        :param request:
        :return:
        """
        if request.user.has_perm('manuscript_record.delete_contributiontypemodel'):
            deleteContributionTypeId = request.data.get('id', None)
            if deleteContributionTypeId:
                deleteContributionTypeResult = json.dumps(
                    deleteSubjectOrTradeContributionTypeTask.delay(options='contribution_type',
                                                                   idOrName=deleteContributionTypeId).get())
                return Response(status=deleteContributionTypeId['status'],
                                data={"message": deleteContributionTypeResult['data']})
            return Response(status=404, data={"message": "缺少部分参数。"})
        return Response(status=403, data={"message": "该用户无相应权限。"})

    def get(self, request):
        """
        获取投稿类型信息
        :param request:
        :return:
        """
        selectContributionTypeTaskResult = json.loads(
            selectSubjectOrTradeOrContributionTypeTask.delay(options='contribution_type').get())
        return Response(status=200, data={"data": selectContributionTypeTaskResult['data']})

    @recode_operation_log(operation='user modify contribution type.', level='warning')
    def put(self, request):
        if request.user.has_perm("manuscript_record.change_contributiontypemodel"):
            updateData = request.data.copy()
            updateData['options'] = 'contribution_type'
            updateTradeTaskResult = json.loads(updateSubjectOrTradeOrContributionTypeTask.delay(**updateData).get())
            return Response(status=updateTradeTaskResult['status'], data={'message': updateTradeTaskResult['data']})
        return Response(status=403, data={"message": "该用户无相应权限。"})


class ManuscriptView(APIView):
    """
    稿件的投递，修改，删除以及查看
    """
    authentication_classes = [TokenAuthenticationRedis]
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """
        作者投递稿件
        :param request:
        :return:
        """
        manuscriptData = request.data.copy().dict()
        manuscriptData['memory_way'] = request.FILES.get('memory_way')
        deliverManuscriptTaskResult = json.loads(deliverManuscriptTask(**manuscriptData))
        return Response(status=deliverManuscriptTaskResult['status'],
                        data={'message': deliverManuscriptTaskResult['data']})

    def get(self, request) -> Response:
        """
        查看作者所有的稿件
        :param request:
        :return:
        """
        username = request.user.__str__()
        orderBy = request.data.get('orderBy', None)
        try:
            userPersonalManuscriptCount, userPersonalManuscript = selectUserPersonalManuscriptTask(username=username,
                                                                                                   order_by=orderBy)
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=userPersonalManuscript, request=request, view=self)
            serializer = ManuscriptModelSerializer(instance=page, many=True)
            return Response(status=200, data={"count": userPersonalManuscriptCount, 'data': serializer.data})
        except:
            return Response(status=403, data={'message': "稿件获取失败！"})

    def delete(self, request) -> Response:
        """
        删除稿件记录，根据实际业务需求，只支持删除未检测和未审核的稿件记录
        :param request:
        :return:
        """
        username = request.user.__str__()
        manuscript_id = request.data.get("manuscript_id", None)
        deleteUserPersonalManuscriptTaskResult = json.loads(
            deleteUserPersonalManuscriptTask.delay(username=username, manuscript_id=manuscript_id).get())
        return Response(status=deleteUserPersonalManuscriptTaskResult['status'],
                        data={"message": deleteUserPersonalManuscriptTaskResult['data']})

    def put(self, request) -> Response:
        """
        修改稿件信息，根据实际业务需求，只支持删除未检测和未审核的稿件记录，以及编辑和审核人员给定修改意见的稿件记录
        :param request:
        :return:
        """
        username = request.user.__str__()
        manuscript_data = request.data.copy().dict()
        manuscript_data['memory_way'] = request.FILES.get('memory_way')
        modifyUserPersonalManuscriptTaskResult = json.loads(
            modifyUserPersonalManuscriptTask(username, **manuscript_data))
        return Response(status=modifyUserPersonalManuscriptTaskResult['status'],
                        data={"message": modifyUserPersonalManuscriptTaskResult['data']})
