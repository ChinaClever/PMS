from django.db import models

# Create your models here.
from application import settings
from application.models import BaseModel


# 模型
# unique：指定该字段的值是否唯一，默认为False，表示允许多个记录具有相同的client_name值。
# blank：指定该字段是否可以为空，默认为True，表示允许该字段的值为空。
# null：指定该字段在数据库中是否允许为空，默认为False，表示不允许该字段的值为空。
class Debug(BaseModel):
    # 工单号
    work_order = models.CharField(max_length=255, verbose_name="工单号", help_text="工单号")
    # 下单日期
    order_time = models.DateTimeField(auto_now_add=False, verbose_name="下单日期", max_length=11)
    # 客户名称
    client_name = models.CharField(max_length=150, verbose_name="客户名称", help_text="客户名称")
    # 规格型号
    shape = models.CharField(max_length=255, verbose_name="规格型号", help_text="规格型号")
    # 产品名称
    product_name = models.CharField(max_length=150, verbose_name="产品名称", help_text="产品名称")
    # 数量
    product_count = models.IntegerField(default=0, verbose_name="数量", help_text="数量")
    # 交期
    submit_time = models.DateTimeField(auto_now_add=False, verbose_name="交期", max_length=11)
    # 开始日期
    start_time = models.DateTimeField(auto_now_add=False, verbose_name="开始日期", max_length=11)
    # 完成日期
    finish_time = models.DateTimeField(auto_now_add=False, verbose_name="开始日期", max_length=11)
    # 所用工时
    work_hours = models.IntegerField(null=True, default=0, verbose_name="所用工时", help_text="所用工时")
    # 具体说明
    instruction = models.CharField(null=True, max_length=150, verbose_name="具体说明", help_text="具体说明")
    # 备注
    remark = models.CharField(null=True, max_length=150, verbose_name="备注", help_text="备注")
    # 成品or模块
    product_module_CHOICES = (
        (1, '成品'),
        (2, '模块')
    )
    product_module = models.IntegerField(choices=product_module_CHOICES,
                                         verbose_name="成品_模块：1-成品 2-模块", help_text="成品_模块：1-成品 2-模块")

class Meta:
        # 数据表名
        db_table = settings.TABLE_PREFIX + "debugreport"
        verbose_name = "调试报表"
        verbose_name_plural = verbose_name

