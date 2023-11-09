# Generated by Django 4.1.3 on 2023-02-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('title', models.CharField(help_text='通知标题', max_length=255, verbose_name='通知标题')),
                ('source', models.IntegerField(choices=[(1, '官方平台'), (2, '开源中国'), (3, 'CSDN官方'), (2, '新浪微博')], default=0, help_text='通知来源：1官方平台 2开源中国 3CSDN官方 4新浪微博', verbose_name='通知来源：1官方平台 2开源中国 3CSDN官方 4新浪微博')),
                ('url', models.CharField(help_text='外部地址', max_length=255, null=True, verbose_name='外部地址')),
                ('click', models.IntegerField(default=0, help_text='点击率', verbose_name='点击率')),
                ('status', models.IntegerField(choices=[(1, '正常'), (2, '停用')], default=1, help_text='通知状态：1-正常 2-停用', verbose_name='通知状态：1-正常 2-停用')),
                ('is_top', models.IntegerField(choices=[(1, '正常'), (2, '停用')], default=1, help_text='是否置顶：1-是 2-否', verbose_name='是否置顶：1-是 2-否')),
                ('content', models.TextField(help_text='通知公告标题', null=True, verbose_name='通知公告标题')),
            ],
            options={
                'verbose_name': '通知公告表',
                'verbose_name_plural': '通知公告表',
                'db_table': 'django_notice',
            },
        ),
    ]
