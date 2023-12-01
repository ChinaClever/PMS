from django.db import models
from application import settings
from config.env import TABLE_PREFIX


class DebugDataTestStep(models.Model):
    # 主键ID
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='主键ID'
    )
    # 调试数据表ID
    debugdata_id = models.IntegerField(default=0, verbose_name="调试数据表ID", help_text="调试数据表ID")
    # 测试步骤编号
    no = models.CharField(null=True, max_length=30, verbose_name="测试步骤编号", help_text="测试步骤编号")
    # 测试步骤名称
    name = models.CharField(null=True, max_length=150, verbose_name="测试步骤名称", help_text="测试步骤名称")
    # 测试步骤结果
    RESULT_CHOICES = ((1, "通过"), (2, "失败"),)
    result = models.IntegerField(null=True, choices=RESULT_CHOICES, default=1, verbose_name="结果：1-通过 2-失败",
                                 help_text="结果：1-通过 2-失败")
    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "debugdata_teststep"
        verbose_name = "调试数据_测试步骤"
        verbose_name_plural = verbose_name


