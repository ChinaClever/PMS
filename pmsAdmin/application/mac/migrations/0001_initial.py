# Generated by Django 4.1.3 on 2023-12-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=255, verbose_name='工单号')),
                ('name', models.CharField(help_text='客户名称', max_length=255, verbose_name='客户名称')),
                ('code', models.CharField(help_text='产品型号', max_length=255, verbose_name='产品型号')),
                ('serial_id', models.CharField(help_text='序列号', max_length=255, null=True, verbose_name='序列号')),
                ('mac_address', models.CharField(help_text='mac地址', max_length=255, null=True, unique=True, verbose_name='mac地址')),
                ('quantity', models.IntegerField(help_text='数量', null=True, verbose_name='数量')),
            ],
            options={
                'verbose_name': 'mac管理表',
                'verbose_name_plural': 'mac管理表',
                'db_table': 'django_mac',
            },
        ),
    ]
