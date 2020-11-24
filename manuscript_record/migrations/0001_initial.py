# Generated by Django 3.1.2 on 2020-11-24 03:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manuscript_review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionTypeModel',
            fields=[
                ('contribution_type_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='投稿类型ID')),
                ('name', models.CharField(max_length=120, verbose_name='投稿类型')),
                ('brief_introduction', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '投稿类型模型',
                'verbose_name_plural': '投稿类型模型',
                'db_table': 'contribution_type_model',
            },
        ),
        migrations.CreateModel(
            name='SubjectModel',
            fields=[
                ('subject_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='研究方向ID')),
                ('name', models.CharField(max_length=150, verbose_name='研究方向')),
                ('brief_introduction', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '研究方向模型',
                'verbose_name_plural': '研究方向模型',
                'db_table': 'subject_model',
            },
        ),
        migrations.CreateModel(
            name='TradeModel',
            fields=[
                ('trade_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='行业领域ID')),
                ('name', models.CharField(max_length=120, verbose_name='行业领域')),
                ('brief_introduction', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '行业领域模型',
                'verbose_name_plural': '行业领域模型',
                'db_table': 'trade_model',
            },
        ),
        migrations.CreateModel(
            name='ManuscriptModel',
            fields=[
                ('manuscript_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='稿件ID')),
                ('title', models.CharField(max_length=256, verbose_name='中文标题')),
                ('title_English', models.CharField(max_length=256, verbose_name='英文标题')),
                ('author', models.CharField(max_length=128, verbose_name='作者姓名')),
                ('author_English', models.CharField(max_length=128, verbose_name='作者姓名（英文）')),
                ('abstract', models.TextField(verbose_name='中文摘要')),
                ('abstract_English', models.TextField(verbose_name='英文摘要')),
                ('keyword', models.CharField(max_length=256, verbose_name='关键字')),
                ('keyword_English', models.CharField(max_length=256, verbose_name='英文关键字')),
                ('textOfManuscript', models.TextField(verbose_name='正文')),
                ('reference', models.TextField(verbose_name='参考文献')),
                ('corresponding_author', models.CharField(max_length=150, verbose_name='通讯作者')),
                ('corresponding_author_contact_way', models.CharField(max_length=64, verbose_name='通讯作者联系方式')),
                ('memory_way', models.FileField(default='default.png', upload_to='manuscript/', verbose_name='稿件')),
                ('contribution_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投递时间')),
                ('check_status', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manuscript_review.checkmanuscriptmodel', verbose_name='稿件检测')),
                ('contribution_type', models.ManyToManyField(to='manuscript_record.ContributionTypeModel', verbose_name='投稿类型')),
                ('review_status', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manuscript_review.reviewmanuscriptmodel', verbose_name='稿件审核')),
                ('subject', models.ManyToManyField(to='manuscript_record.SubjectModel', verbose_name='研究方向')),
                ('trade', models.ManyToManyField(to='manuscript_record.TradeModel', verbose_name='行业领域')),
            ],
            options={
                'verbose_name': '稿件模型',
                'verbose_name_plural': '稿件模型',
                'db_table': 'manuscript_model',
            },
        ),
    ]