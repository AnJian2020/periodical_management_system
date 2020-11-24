from django.db import models
from django.utils import timezone


class CheckManuscriptModel(models.Model):
    """
    稿件检测信息模型
    """
    id = models.CharField(max_length=25, primary_key=True, verbose_name="id")
    check_name = models.CharField(max_length=150, verbose_name="检测人员姓名")
    check_contact_way = models.CharField(max_length=64, verbose_name="检测人员联系方式")
    duplicate_checking_rate = models.FloatField(verbose_name="查重率")
    multiple_contributions_to_one_manuscript = models.BooleanField(verbose_name="是否一稿多投")
    is_subject = models.BooleanField(verbose_name="研究方向是否相符")
    is_contribution = models.BooleanField(verbose_name="投稿类型是否相符")
    is_trade = models.BooleanField(verbose_name="行业领域是否相符")
    check_result = models.CharField(verbose_name="检测结果", max_length=16)
    check_time = models.DateTimeField(verbose_name="检测时间", default=timezone.now)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '稿件检测mx'
        verbose_name_plural = '稿件检测信息表'
        db_table = 'check_manuscript_model'


class ReviewManuscriptModel(models.Model):
    """
    稿件审核信息模型
    """
    id = models.CharField(max_length=20, primary_key=True, verbose_name="id")
    # 初审
    preliminary_result = models.CharField(verbose_name='初审结果', max_length=16, null=True, blank=True)
    preliminary_evaluation = models.TextField(verbose_name='初审评价', blank=True, null=True)
    preliminary_user = models.CharField(verbose_name="初审人员", max_length=150, null=True, blank=True)
    preliminary_user_contact_way = models.CharField(verbose_name='初审人员联系方式', max_length=64, null=True,
                                                    blank=True)
    preliminary_time = models.DateTimeField(verbose_name='初审时间', null=True, blank=True)
    preliminary_deadline = models.DateTimeField(verbose_name="初审截止时间", null=True, blank=True)
    # 外审
    # 外审只是参考，无法决定稿件是否通过，故暂时取消外审结果字段
    # external_audit_result=models.CharField(verbose_name='external audit status',max_length=16,null=True,blank=True)
    external_audit_evaluation = models.TextField(verbose_name="外审评价", null=True, blank=True)
    external_audit_user = models.CharField(verbose_name="外审人员", max_length=150, null=True, blank=True)
    external_audit_user_contact_way = models.CharField(verbose_name='外审人员联系方式', max_length=64, null=True,
                                                       blank=True)
    external_audit_time = models.DateTimeField(verbose_name='外审时间', null=True, blank=True)
    external_audit_deadline = models.DateTimeField(verbose_name='外审截止时间', null=True, blank=True)
    # 复审
    review_result = models.CharField(verbose_name='复审结果', max_length=16, null=True, blank=True)
    review_evaluation = models.TextField(verbose_name='复审评价', null=True, blank=True)
    review_user = models.CharField(verbose_name='复审人员', max_length=150, null=True, blank=True)
    review_user_contact_way = models.CharField(verbose_name='复审人员联系方式', max_length=64, null=True, blank=True)
    review_time = models.DateTimeField(verbose_name='复审时间', null=True, blank=True)
    review_deadline = models.DateTimeField(verbose_name='复审截止时间', null=True, blank=True)
    # 终审
    final_judgment_result = models.CharField(verbose_name='终审结果', max_length=16, null=True, blank=True)
    final_judgment_evaluation = models.TextField(verbose_name='终审评价', null=True, blank=True)
    final_judgment_user = models.CharField(verbose_name='终审人员', max_length=150, null=True, blank=True)
    final_judgment_user_contact_way = models.CharField(verbose_name='终审人员联系方式', max_length=64, null=True,
                                                       blank=True)
    final_judgment_time = models.DateTimeField(verbose_name='终审时间', null=True, blank=True)
    final_judgment_deadline = models.DateTimeField(verbose_name='终审截止时间', null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '稿件审核模型'
        verbose_name_plural = '稿件审核模型'
        db_table = 'review_manuscript_model'
