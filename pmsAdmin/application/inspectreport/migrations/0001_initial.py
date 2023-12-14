# Generated by Django 4.1.3 on 2023-12-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inspectreport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('create_user', models.IntegerField(default=0, verbose_name='创建人')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=11, null=True, verbose_name='创建时间')),
                ('update_user', models.IntegerField(default=0, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, max_length=11, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=0, verbose_name='逻辑删除')),
                ('work_order', models.CharField(help_text='工单号', max_length=255, verbose_name='工单号')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('product_name', models.CharField(help_text='产品名称', max_length=255, verbose_name='产品名称')),
                ('commit_user', models.CharField(help_text='填写者', max_length=255, verbose_name='填写者')),
                ('item_number', models.CharField(help_text='产品型号', max_length=255, verbose_name='产品型号')),
                ('examine_an_amount', models.IntegerField(help_text='检验数量', verbose_name='检验数量')),
                ('examine_a_bad_amount', models.IntegerField(help_text='检验不良数量', verbose_name='检验不良数量')),
                ('examine_amount_total_amount', models.IntegerField(help_text='检验数量累计', verbose_name='检验数量累计')),
                ('examine_bad_total_amount', models.IntegerField(help_text='检验不良累计', verbose_name='检验不良累计')),
                ('target_pass_rate', models.IntegerField(help_text='ERP目标合格率', verbose_name='ERP目标合格率')),
                ('target_actual_pass_rate', models.IntegerField(help_text='实际合格率', verbose_name='实际合格率')),
                ('signal', models.IntegerField(choices=[(1, '红色'), (2, '绿色')], default=1, help_text='信号：1-红色 2-绿色', verbose_name='信号：1-红色 2-绿色')),
                ('product_module', models.IntegerField(choices=[(1, '成品'), (2, '模块')], default=1, help_text='成品/模块：1-成品 2-模块', verbose_name='成品/模块：1-成品 2-模块')),
                ('problem', models.TextField(help_text='问题', null=True, verbose_name='问题')),
                ('action', models.TextField(help_text='行动', null=True, verbose_name='行动')),
                ('work_hours', models.IntegerField(help_text='工时', verbose_name='工时')),
            ],
            options={
                'verbose_name': '质检报表',
                'verbose_name_plural': '质检报表',
                'db_table': 'django_inspectreport',
            },
        ),
    ]
