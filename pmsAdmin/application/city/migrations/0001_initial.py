# Generated by Django 4.1.3 on 2023-02-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('city_code', models.CharField(help_text='城市区号', max_length=6, verbose_name='城市区号')),
                ('area_code', models.CharField(help_text='行政编码', max_length=20, verbose_name='行政编码')),
                ('parent_code', models.CharField(help_text='上级行政编码', max_length=20, null=True, verbose_name='上级行政编码')),
                ('zip_code', models.CharField(help_text='邮政编码', max_length=6, verbose_name='邮政编码')),
                ('level', models.IntegerField(default=0, help_text='城市级别：1-省份 2-城市 3-县区 4-街道', verbose_name='城市级别：1-省份 2-城市 3-县区 4-街道')),
                ('pid', models.IntegerField(default=0, help_text='上级城市ID', verbose_name='上级城市ID')),
                ('name', models.CharField(help_text='城市名称', max_length=150, verbose_name='城市名称')),
                ('short_name', models.CharField(help_text='城市简称', max_length=150, verbose_name='城市简称')),
                ('full_name', models.CharField(help_text='城市全称', max_length=150, null=True, verbose_name='城市全称')),
                ('pinyin', models.CharField(help_text='城市拼音', max_length=150, null=True, verbose_name='城市拼音')),
                ('lng', models.CharField(help_text='城市经度', max_length=150, null=True, verbose_name='城市经度')),
                ('lat', models.CharField(help_text='城市纬度', max_length=150, null=True, verbose_name='城市纬度')),
            ],
            options={
                'verbose_name': '城市表',
                'verbose_name_plural': '城市表',
                'db_table': 'django_city',
            },
        ),
    ]
