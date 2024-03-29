# Generated by Django 4.1.3 on 2023-12-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Welding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=255, verbose_name='工单号')),
                ('order_time', models.DateTimeField(max_length=11, verbose_name='下单日期')),
                ('client_name', models.CharField(help_text='客户名称', max_length=255, verbose_name='客户名称')),
                ('shape', models.CharField(help_text='规格型号', max_length=255, verbose_name='规格型号')),
                ('product_name', models.CharField(help_text='产品名称', max_length=255, verbose_name='产品名称')),
                ('product_count', models.IntegerField(default=0, help_text='数量', verbose_name='数量')),
                ('submit_time', models.DateTimeField(max_length=11, verbose_name='交期')),
                ('instruction', models.CharField(help_text='具体说明', max_length=255, null=True, verbose_name='具体说明')),
                ('remark', models.CharField(help_text='备注', max_length=255, null=True, verbose_name='备注')),
                ('start_time', models.DateTimeField(max_length=11, verbose_name='开始日期')),
                ('finish_time', models.DateTimeField(max_length=11, verbose_name='开始日期')),
                ('work_hours', models.IntegerField(default=0, help_text='所用工时', null=True, verbose_name='所用工时')),
                ('welding_count', models.IntegerField(default=0, help_text='焊接数量', verbose_name='焊接数量')),
            ],
            options={
                'verbose_name': '焊接报表',
                'verbose_name_plural': '焊接报表',
                'db_table': 'django_weldingreport',
            },
        ),
    ]
