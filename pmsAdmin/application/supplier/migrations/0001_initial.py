# Generated by Django 4.1.3 on 2023-12-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=150, null=True, verbose_name='工单号')),
                ('customer', models.CharField(help_text='客户', max_length=150, null=True, verbose_name='客户')),
                ('product_name', models.CharField(help_text='产品', max_length=150, null=True, verbose_name='产品')),
                ('product_type', models.CharField(help_text='产品类型', max_length=150, null=True, verbose_name='产品类型')),
                ('supplier', models.CharField(help_text='供应商', max_length=150, verbose_name='供应商')),
                ('parts', models.CharField(help_text='部件', max_length=150, verbose_name='部件')),
                ('product_number', models.IntegerField(help_text='数量', verbose_name='数量')),
                ('notes', models.CharField(help_text='备注', max_length=150, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '供应商管理',
                'verbose_name_plural': '供应商管理',
                'db_table': 'django_supplier',
            },
        ),
    ]
