from django.db import models
from application import settings

class Module(models.Model):
    # 主键ID
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='主键ID'
    )
    # 成品序列Id
    product_id = models.IntegerField(default=0, verbose_name="成品序列Id", help_text="成品序列Id")
    # 模块码
    module_SN = models.CharField(max_length=255, verbose_name="模块码", help_text="模块码")

    class Meta:
        # 数据表名
        db_table = settings.TABLE_PREFIX + "bind_module"
        verbose_name = "模块"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '模块{}'.format(self.name)

