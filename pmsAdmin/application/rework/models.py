from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from application.models import BaseModel
from config.env import TABLE_PREFIX


# 通知公告模型
class Rework(BaseModel):

    work_order = models.CharField(null=False, max_length=255,verbose_name="工单号", help_text="工单号")

    # 产品名称
    product_name = models.CharField(max_length=255, verbose_name="产品名称", help_text="产品名称")

    respon = models.CharField(null=False, max_length=255, verbose_name="责任归属人", help_text="责任归属人")

    item_number = models.CharField(null=False, max_length=255, verbose_name="产品型号", help_text="产品型号")

    rw_qty = models.IntegerField(null=False, verbose_name="返工数量", help_text="返工数量")

    loss_time = models.IntegerField(null=False, verbose_name="损耗工时", help_text="损耗工时")

    loss_material_qty = models.IntegerField(null=False, verbose_name="损耗材料数量", help_text="损耗材料数量")

    loss_material_name = models.CharField(null=False, max_length=255, verbose_name="损耗材料名称", help_text="损耗材料名称")

    RW_REASON_CHOICES = (
        (1, "物料不良/半成品/成品返工工时"),
        (2, "返工/正常作业/原料报废"),
        (3, "客户退回产品的维修"),
    )

    rw_reason = models.IntegerField(choices=RW_REASON_CHOICES, default=1, verbose_name="返工原因：1-物料不良/半成品/成品返工工时 2-返工/正常作业/原料报废 3-客户退回产品的维修",
                                 help_text="返工原因：1-物料不良/半成品/成品返工工时 2-返工/正常作业/原料报废 3-客户退回产品的维修")

    PRODUCT_MODULE_CHOICES = (
        (1,"成品"),
        (2,"模块")
    )

    product_module = models.IntegerField(choices=PRODUCT_MODULE_CHOICES, default=1, verbose_name="成品/模块：1-成品 2-模块",
                                 help_text="成品/模块：1-成品 2-模块")
    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "rework"
        verbose_name = "返工记录表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "返工记录表{}".format(self.title)