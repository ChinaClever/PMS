from django.db import models
from application.models import BaseModel
from config.env import TABLE_PREFIX

class Shipment(BaseModel):
    # 工单号
    work_order = models.CharField(max_length=255, verbose_name="工单号", help_text="工单号")
    # 客户名称
    client_name = models.CharField(max_length=255, verbose_name="客户名称", help_text="客户名称")
    # 成品编码
    product_code = models.CharField(max_length=255, verbose_name="成品编码", help_text="成品编码")
    # 产品名称（下拉框 数据大写）
    product_name = models.CharField(max_length=255, verbose_name="产品名称", help_text="产品名称")
    # 规格型号
    shape = models.CharField(max_length=255, verbose_name="规格型号", help_text="规格型号")
    # 订单日期
    order_date = models.DateTimeField(auto_now_add=False, verbose_name="订单日期", max_length=11)
    # 交货日期
    delivery_date  = models.DateTimeField(auto_now_add=False, verbose_name="交货日期", max_length=11)
    # 更改交期
    update_delivery_date = models.DateTimeField(null=True, auto_now_add=False, verbose_name="更改交货日期", max_length=11)
    # 完成日期
    finish_date = models.DateTimeField(null=True, auto_now_add=False, verbose_name="完成日期", max_length=11)
    # 数量
    product_count = models.IntegerField(default=0, verbose_name="数量", help_text="数量")
    # SO_RQ号
    SO_RQ_id = models.CharField(max_length=255, verbose_name="SO_RQ号", help_text="SO_RQ号")
    # 备注
    remark = models.CharField(null=True, max_length=255, verbose_name="备注", help_text="备注")
    # 成品or模块
    product_module_CHOICES = (
        (1, '成品'),
        (2, '模块')
    )
    product_module = models.IntegerField(null=False, choices=product_module_CHOICES, verbose_name="成品_模块：1-成品 2-模块", help_text="成品_模块：1-成品 2-模块")
    # 附件
    attachment = models.CharField(null=True, max_length=255, verbose_name="附件", help_text="附件")

    class Meta:
        db_table = TABLE_PREFIX + 'shipmentreport'
        verbose_name = '排期表单表'
        verbose_name_plural = verbose_name

# 产品关联表
class Product(BaseModel):
    # 成品编码
    product_code = models.CharField(null=False, max_length=255, verbose_name="成品编码", help_text="成品编码")
    # 产品名称（下拉框 数据大写）
    product_name = models.CharField(null=False, max_length=255, verbose_name="产品名称", help_text="产品名称")
    # 规格型号
    shape = models.CharField(max_length=255, verbose_name="规格型号", help_text="规格型号")
    # 成品or模块
    product_module_CHOICES = (
        (1, '成品'),
        (2, '模块')
    )
    product_module = models.IntegerField(null=False, choices=product_module_CHOICES,
                                         verbose_name="成品_模块：1-成品 2-模块", help_text="成品_模块：1-成品 2-模块")
    class Meta:
        db_table = TABLE_PREFIX + 'product'
        verbose_name = '产品关联表'
        verbose_name_plural = verbose_name