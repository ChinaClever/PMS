from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from application.models import BaseModel
from config.env import TABLE_PREFIX


# 通知公告模型
class Followup(BaseModel):

    work_order = models.CharField(null=False, max_length=255,verbose_name="工单号", help_text="工单号")

    start_time = models.DateTimeField(
        verbose_name="开始时间",
    )

    end_time = models.DateTimeField(
        verbose_name="结束时间",
    )

    # 产品名称
    product_name = models.CharField(max_length=255, verbose_name="产品名称", help_text="产品名称")

    commit_user = models.CharField(null=False, max_length=255, verbose_name="填写者", help_text="填写者")

    item_number = models.CharField(null=False, max_length=255, verbose_name="产品型号", help_text="产品型号")

    qty_obj_hour = models.IntegerField(null=False, verbose_name="ERP目标", help_text="ERP目标")

    qty_prod_hour = models.IntegerField(null=False, verbose_name="实际产出", help_text="实际产出")

    cumul_qty_obj = models.IntegerField(null=False, verbose_name="ERP目标累计", help_text="ERP目标累计")

    cumul_qty_prod = models.IntegerField(null=False, verbose_name="实际累计", help_text="实际累计")

    loss_time = models.IntegerField(null=False, verbose_name="损耗工时", help_text="损耗工时")

    changeover_time = models.IntegerField(null=False, verbose_name="换线时间", help_text="换线时间")

    SIGNAL_CHOICES = (
        (1, "红色"),
        (2, "绿色"),
    )

    signal = models.IntegerField(choices=SIGNAL_CHOICES, default=1, verbose_name="信号：1-红色 2-绿色",
                                 help_text="信号：1-红色 2-绿色")

    PRODUCT_MODULE_CHOICES = (
        (1,"成品"),
        (2,"模块")
    )

    product_module = models.IntegerField(choices=PRODUCT_MODULE_CHOICES, default=1, verbose_name="成品/模块：1-成品 2-模块",
                                 help_text="成品/模块：1-成品 2-模块")
    problem = models.TextField(null=True, verbose_name="问题", help_text="问题")

    action = models.TextField(null=True, verbose_name="行动", help_text="行动")

    remark = models.TextField(null=True, verbose_name="备注", help_text="备注")

    work_hours = models.IntegerField(null=False, verbose_name="工时", help_text="工时")
    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "followup"
        verbose_name = "组装跟进表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "组装跟进表{}".format(self.title)