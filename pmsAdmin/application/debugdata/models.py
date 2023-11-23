from django.db import models

from application import settings
from application.models import BaseModel

class Debugdata(BaseModel):
    # 软件类型
    softwareType = models.CharField(max_length=150, verbose_name="软件类型", help_text="软件类型")
    # 产品类型
    productType = models.CharField(max_length=150, verbose_name="产品类型", help_text="产品类型")
    # 产品SN
    productSN = models.CharField(max_length=150, verbose_name="产品SN", help_text="产品SN")
    # mac地址
    macAddress = models.CharField(max_length=150, verbose_name="mac地址", help_text="mac地址")
    # 结果
    RESULT_CHOICES = ( (1, "通过"), (2, "失败"), )
    result = models.IntegerField(choices=RESULT_CHOICES, default=1, verbose_name="结果：1-通过 2-失败",
                                 help_text="结果：1-通过 2-失败")
    # 软件版本
    softwareVersion = models.CharField(max_length=30, verbose_name="软件版本", help_text="软件版本")
    # 客户名称
    clientName = models.CharField(max_length=150, verbose_name="客户名称", help_text="客户名称")
    # 公司名
    companyName = models.CharField(max_length=150, verbose_name="公司名", help_text="公司名")
    # 协议版本
    protocolVersion = models.CharField(max_length=30, verbose_name="协议版本", help_text="协议版本")
    # 测试开始时间
    testStartTime = models.DateTimeField(auto_now_add=False, verbose_name="测试开始时间", max_length=11)
    # 测试结束时间
    testEndTime = models.DateTimeField(auto_now_add=False, verbose_name="测试结束时间", max_length=11)
    # 测试时间
    testTime = models.CharField(max_length=150, verbose_name="测试时间", help_text="测试时间")

    class Meta:
        # 数据表名
        db_table = settings.TABLE_PREFIX + "debugdata"
        verbose_name = "调试数据"
        verbose_name_plural = verbose_name

