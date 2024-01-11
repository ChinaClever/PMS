from django.db import models

from application.models import BaseModel
from config.env import TABLE_PREFIX


class Debugdata(BaseModel):
    # 软件类型
    softwareType = models.CharField(null=True, max_length=255, verbose_name="软件类型", help_text="软件类型")
    # 产品类型
    productType = models.CharField(null=True, max_length=255, verbose_name="产品类型", help_text="产品类型")
    # 模块SN
    productSN = models.CharField(null=True, max_length=255, verbose_name="模块SN", help_text="模块SN")
    # mac地址
    macAddress = models.CharField(null=True, max_length=255, verbose_name="mac地址", help_text="mac地址")
    # 结果
    RESULT_CHOICES = ( (1, "通过"), (2, "失败"), )
    result = models.IntegerField(null=True, choices=RESULT_CHOICES, default=1, verbose_name="结果：1-通过 2-失败",
                                 help_text="结果：1-通过 2-失败")
    # 软件版本
    softwareVersion = models.CharField(null=True, max_length=255, verbose_name="软件版本", help_text="软件版本")
    # 单号
    work_order = models.CharField(null=False, max_length=255, verbose_name="工单号", help_text="工单号")
    # 公司名
    companyName = models.CharField(null=True, max_length=255, verbose_name="公司名", help_text="公司名")
    # 协议版本
    protocolVersion = models.CharField(null=True, max_length=255, verbose_name="协议版本", help_text="协议版本")
    # 测试开始时间
    testStartTime = models.DateTimeField(null=True, auto_now_add=False, verbose_name="测试开始时间", max_length=11)
    # 测试结束时间
    testEndTime = models.DateTimeField(null=True, auto_now_add=False, verbose_name="测试结束时间", max_length=11)
    # 测试时间
    testTime = models.CharField(null=True, max_length=255, verbose_name="测试时间", help_text="测试时间")
    # PCB码
    PCB_Code = models.CharField(null=True, max_length=255, verbose_name="PCB码", help_text="PCB码")

    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "debugdata"
        verbose_name = "调试数据"
        verbose_name_plural = verbose_name

