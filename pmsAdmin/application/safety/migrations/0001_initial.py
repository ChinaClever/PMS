# Generated by Django 4.1.3 on 2023-12-14 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='safety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=255, verbose_name='工单号')),
                ('softwareType', models.CharField(help_text='软件类型', max_length=255, verbose_name='软件类型')),
                ('productType', models.CharField(help_text='产品类型', max_length=255, verbose_name='产品类型')),
                ('productSN', models.CharField(help_text='产品序列号', max_length=255, null=True, verbose_name='产品序列号')),
                ('Gnd', models.CharField(help_text='接地电阻', max_length=255, null=True, verbose_name='接地电阻')),
                ('Ir', models.CharField(help_text='绝缘电阻', max_length=255, null=True, verbose_name='绝缘电阻')),
                ('Dcw', models.CharField(help_text='直流耐压', max_length=255, null=True, verbose_name='直流耐压')),
                ('Acw', models.CharField(help_text='交流耐压', max_length=255, null=True, verbose_name='交流耐压')),
                ('result', models.CharField(help_text='结果', max_length=255, null=True, verbose_name='结果')),
                ('softwareVersion', models.CharField(help_text='软件版本', max_length=255, null=True, verbose_name='软件版本')),
                ('companyName', models.CharField(help_text='公司名称', max_length=255, null=True, verbose_name='公司名称')),
                ('protocolVersion', models.CharField(help_text='协议版本', max_length=255, null=True, verbose_name='协议版本')),
                ('testStartTime', models.DateTimeField(help_text='测试开始时间', max_length=150, verbose_name='测试开始时间')),
                ('testEndTime', models.DateTimeField(help_text='测试结束时间', max_length=150, verbose_name='测试结束时间')),
                ('testTime', models.DateTimeField(help_text='测试时间', max_length=150, verbose_name='测试时间')),
            ],
            options={
                'verbose_name': '安规管理表',
                'verbose_name_plural': '安规管理表',
                'db_table': 'django_safety',
            },
        ),
    ]
