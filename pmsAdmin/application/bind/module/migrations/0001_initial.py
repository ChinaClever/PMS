# Generated by Django 4.1.3 on 2024-01-11 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='主键ID')),
                ('product_id', models.IntegerField(default=0, help_text='成品序列号Id', verbose_name='成品序列号Id')),
                ('key', models.CharField(help_text='测试步骤编号', max_length=255, verbose_name='测试步骤编号')),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块',
                'db_table': 'django_bind_module',
            },
        ),
    ]
