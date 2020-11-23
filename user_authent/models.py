from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone


class UserInformation(models.Model):
    """
    用户信息模型
    """
    id=models.AutoField(primary_key=True)
    username=models.ForeignKey(User,to_field='username',on_delete=models.CASCADE)
    real_name = models.CharField(max_length=150, verbose_name='真实姓名')
    sex = models.BooleanField(verbose_name='性别')
    birthday = models.DateField(verbose_name='出生日期')
    politic_countenance = models.CharField(max_length=64, verbose_name="政治面貌")
    marital_status = models.CharField(max_length=32, verbose_name="婚姻状况")
    academic_qualification = models.CharField(max_length=32, verbose_name="学历")
    contact_way = models.CharField(max_length=64, blank=True, null=True, verbose_name='联系方式')
    email = models.EmailField(verbose_name="电子邮箱")
    certificate_type = models.CharField(max_length=32, verbose_name="证件类型")
    certificate_number = models.CharField(max_length=32, verbose_name="证件号码")
    age = models.IntegerField(verbose_name="年龄")
    graduate_school = models.CharField(max_length=64,verbose_name="毕业院校")
    graduate_time = models.DateField(verbose_name="毕业时间")
    graduate_speciality = models.CharField(max_length=64,verbose_name="专业")
    adress = models.CharField(max_length=128, blank=True, null=True, verbose_name='家庭地址')
    postal_code = models.CharField(max_length=12, null=True, blank=True, verbose_name='邮编')
    work_unit = models.CharField(max_length=256, null=True, blank=True, verbose_name='工作单位')
    resume = models.TextField(null=True, blank=True, verbose_name='个人简介')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'user_information'
        verbose_name = '用户信息模型'
        verbose_name_plural = '用户信息模型'


class UserMenuModel(models.Model):
    """
    用户菜单模型
    """
    id=models.AutoField(primary_key=True)
    menu_name=models.CharField(max_length=128,verbose_name="名称",unique=True)
    menu_level=models.IntegerField(verbose_name="级别")
    parent_menu=models.ForeignKey(to='self',null=True,blank=True,on_delete=models.CASCADE)
    # child_menu=models.ManyToManyField(to='self',db_table='menu_relationship',null=True,blank=True)
    menu_path=models.CharField(max_length=128,verbose_name="路由地址")
    menu_role=models.ManyToManyField(Group,through='GroupMenuShip',related_name="group_menu_ship")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table='user_menu_model'
        verbose_name='用户菜单模型'
        verbose_name_plural='用户菜单模型'

class GroupMenuShip(models.Model):
    id=models.AutoField(primary_key=True)
    menu_id=models.ForeignKey(UserMenuModel,on_delete=models.CASCADE)
    group_id=models.ForeignKey(Group,on_delete=models.CASCADE)
    create_time=models.DateTimeField(default=timezone.now)


