from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from application.models import BaseModel
from config.env import TABLE_PREFIX


# 通知公告模型
class Inspectreport(BaseModel):

    work_order = models.CharField(null=False, max_length=255,verbose_name="工单号", help_text="工单号")

    start_time = models.DateTimeField(
        verbose_name="开始时间",
    )

    end_time = models.DateTimeField(
        verbose_name="结束时间",
    )

    commit_user = models.CharField(null=False, max_length=40, verbose_name="填写者", help_text="填写者")

    item_number = models.CharField(null=False, max_length=40, verbose_name="产品型号", help_text="产品型号")

    examine_an_amount = models.IntegerField(null=False, verbose_name="检验数量", help_text="检验数量")

    examine_a_bad_amount = models.IntegerField(null=False, verbose_name="检验不良数量", help_text="检验不良数量")

    examine_amount_total_amount = models.IntegerField(null=False, verbose_name="检验数量累计", help_text="检验数量累计")

    examine_bad_total_amount = models.IntegerField(null=False, verbose_name="检验不良累计", help_text="检验不良累计")

    target_pass_rate = models.IntegerField(null=False, verbose_name="ERP目标合格率", help_text="ERP目标合格率")

    target_actual_pass_rate = models.IntegerField(null=False, verbose_name="实际合格率", help_text="实际合格率")

    SIGNAL_CHOICES = (
        (1, "红色"),
        (2, "绿色"),
    )

    signal = models.IntegerField(choices=SIGNAL_CHOICES, default=1, verbose_name="信号：1-红色 2-绿色",
                                 help_text="信号：1-红色 2-绿色")

    problem = models.TextField(null=True, verbose_name="问题", help_text="问题")

    action = models.TextField(null=True, verbose_name="行动", help_text="行动")

    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "inspectreport"
        verbose_name = "质检报表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "质检报表{}".format(self.title)