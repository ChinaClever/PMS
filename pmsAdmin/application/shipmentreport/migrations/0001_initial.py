# Generated by Django 4.1.3 on 2023-12-04 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('product_code', models.CharField(help_text='成品编码', max_length=255, verbose_name='成品编码')),
                ('product_name', models.CharField(help_text='产品名称', max_length=255, verbose_name='产品名称')),
                ('shape', models.CharField(help_text='规格型号', max_length=255, verbose_name='规格型号')),
                ('product_module', models.IntegerField(choices=[(1, '成品'), (2, '模块')], help_text='成品_模块：1-成品 2-模块', verbose_name='成品_模块：1-成品 2-模块')),
            ],
            options={
                'verbose_name': '产品关联表',
                'verbose_name_plural': '产品关联表',
                'db_table': 'django_product',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=255, verbose_name='工单号')),
                ('client_name', models.CharField(help_text='客户名称', max_length=255, verbose_name='客户名称')),
                ('product_code', models.CharField(help_text='成品编码', max_length=255, verbose_name='成品编码')),
                ('product_name', models.CharField(help_text='产品名称', max_length=255, verbose_name='产品名称')),
                ('shape', models.CharField(help_text='规格型号', max_length=255, verbose_name='规格型号')),
                ('order_date', models.DateTimeField(max_length=11, verbose_name='订单日期')),
                ('delivery_date', models.DateTimeField(max_length=11, verbose_name='交货日期')),
                ('update_delivery_date', models.DateTimeField(max_length=11, null=True, verbose_name='更改交货日期')),
                ('finish_date', models.DateTimeField(max_length=11, null=True, verbose_name='完成日期')),
                ('product_count', models.IntegerField(default=0, help_text='数量', verbose_name='数量')),
                ('SO_RQ_id', models.CharField(help_text='SO_RQ号', max_length=255, verbose_name='SO_RQ号')),
                ('remark', models.CharField(help_text='备注', max_length=255, null=True, verbose_name='备注')),
                ('product_module', models.IntegerField(choices=[(1, '成品'), (2, '模块')], help_text='成品_模块：1-成品 2-模块', verbose_name='成品_模块：1-成品 2-模块')),
                ('attachment', models.CharField(help_text='附件', max_length=255, null=True, verbose_name='附件')),
            ],
            options={
                'verbose_name': '排期表单表',
                'verbose_name_plural': '排期表单表',
                'db_table': 'django_shipmentreport',
            },
        ),
    ]
