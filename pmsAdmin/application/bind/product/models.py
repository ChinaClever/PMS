from django.db import models

from application import settings
from application.models import BaseModel

class ProductBind(BaseModel):
    # 序列号
    goods_SN = models.CharField(max_length=255, verbose_name="序列号", help_text="序列号")

    class Meta:
        # 数据表名
        db_table = settings.TABLE_PREFIX + "bind_product"
        verbose_name = "成品序列号"
        verbose_name_plural = verbose_name

