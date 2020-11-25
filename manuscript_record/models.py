from django.db import models
from django.utils import timezone
from manuscript_review.models import CheckManuscriptModel,ReviewManuscriptModel


class SubjectModel(models.Model):
    """
    研究方向模型
    """
    id = models.CharField(verbose_name="研究方向ID", primary_key=True, max_length=25)
    name = models.CharField(verbose_name="研究方向", max_length=150)
    brief_introduction = models.TextField(verbose_name="简介", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "研究方向模型"
        verbose_name_plural = "研究方向模型"
        db_table = 'subject_model'


class ContributionTypeModel(models.Model):
    """
    投稿类型模型
    """
    id = models.CharField(verbose_name="投稿类型ID", primary_key=True, max_length=25)
    name = models.CharField(verbose_name="投稿类型", max_length=120)
    brief_introduction = models.TextField(verbose_name="简介", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "投稿类型模型"
        verbose_name_plural = "投稿类型模型"
        db_table = "contribution_type_model"


class TradeModel(models.Model):
    """
    行业领域模型
    """
    id = models.CharField(max_length=25, primary_key=True, verbose_name="行业领域ID")
    name = models.CharField(verbose_name="行业领域", max_length=120)
    brief_introduction = models.TextField(verbose_name="简介", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "行业领域模型"
        verbose_name_plural = "行业领域模型"
        db_table = 'trade_model'


class ManuscriptModel(models.Model):
    """
    稿件信息模型
    """
    manuscript_id = models.CharField(verbose_name="稿件ID", max_length=25, primary_key=True)
    title = models.CharField(max_length=256, verbose_name="中文标题")
    title_English = models.CharField(max_length=256, verbose_name="英文标题")
    author = models.CharField(max_length=128, verbose_name="作者姓名")
    author_English = models.CharField(max_length=128, verbose_name="作者姓名（英文）")
    abstract = models.TextField(verbose_name="中文摘要")
    abstract_English = models.TextField(verbose_name="英文摘要")
    keyword = models.CharField(max_length=256, verbose_name="关键字")
    keyword_English = models.CharField(max_length=256, verbose_name="英文关键字")
    textOfManuscript = models.TextField(verbose_name="正文")
    reference = models.TextField(verbose_name="参考文献")
    corresponding_author = models.CharField(verbose_name="通讯作者", max_length=150)
    corresponding_author_contact_way = models.CharField(verbose_name="通讯作者联系方式", max_length=64)

    subject = models.ManyToManyField(
        SubjectModel,
        verbose_name="研究方向")
    contribution_type = models.ManyToManyField(
        ContributionTypeModel,
        verbose_name="投稿类型")
    trade = models.ManyToManyField(
        TradeModel,
        verbose_name="行业领域")

    memory_way = models.FileField(verbose_name="稿件",upload_to='manuscript/',default="default.png")

    contribution_time = models.DateTimeField(default=timezone.now, verbose_name="投递时间")

    check_status = models.OneToOneField(
        CheckManuscriptModel,
        on_delete=models.CASCADE,
        verbose_name="稿件检测",
        null=True, blank=True
    )
    review_status = models.OneToOneField(
        ReviewManuscriptModel,
        on_delete=models.CASCADE,
        verbose_name="稿件审核",
        null=True, blank=True
    )

    def __str__(self):
        return self.manuscript_id

    class Meta:
        verbose_name = "稿件模型"
        verbose_name_plural = "稿件模型"
        db_table='manuscript_model'



