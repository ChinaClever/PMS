# Generated by Django 4.1.3 on 2023-11-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='burning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=150, verbose_name='工单号')),
                ('name', models.CharField(help_text='客户名称', max_length=6, verbose_name='客户名称')),
                ('code', models.CharField(help_text='规格型号', max_length=20, verbose_name='规格型号')),
                ('version', models.CharField(help_text='版本号', max_length=20, null=True, verbose_name='版本号')),
                ('require', models.CharField(help_text='程序要求', max_length=6, verbose_name='程序要求')),
                ('order_time', models.DateTimeField(help_text='订单日期', max_length=18, verbose_name='订单日期')),
                ('delivery_time', models.DateTimeField(help_text='交货日期', max_length=18, null=True, verbose_name='交货日期')),
                ('quantity', models.IntegerField(help_text='数量', null=True, verbose_name='数量')),
                ('remark', models.CharField(help_text='备注', max_length=150, null=True, verbose_name='备注')),
                ('rcerder', models.CharField(help_text='rcerder', max_length=150, null=True, verbose_name='rcerder')),
            ],
            options={
                'verbose_name': '烧录表',
                'verbose_name_plural': '烧录表',
                'db_table': 'django_burning',
            },
        ),
    ]