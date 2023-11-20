from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from application.models import BaseModel
from config.env import TABLE_PREFIX


# 通知公告模型
class Suggestion(BaseModel):

    content = models.TextField(null=True, verbose_name="需求或建议", help_text="需求或建议")

    commit_user = models.CharField(null=True, max_length=40, verbose_name="提交者", help_text="提交者")

    STATUS_CHOICES = (
        (1, "未查看"),
        (2, "确认"),
        (3, "完成"),
        (4, "不通过")
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="处理状态：1-未查看 2-确认 3-完成 4-未通过",
                                 help_text="处理状态：1-未查看 2-确认 3-完成 4-未通过")

    TYPE_CHOICES = (
        (1, "问题"),
        (2, "建议"),
        (3, "新需求")
    )

    type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="类型：1-问题 2-建议 3-新需求 ",
                                 help_text="类型：1-问题 2-建议 3-新需求 ")

    feedback = models.TextField(verbose_name="反馈内容",help_text="反馈内容")

    priority = models.IntegerField(default=10,verbose_name="优先级",help_text="优先级")


    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "suggestion"
        verbose_name = "意见反馈"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "意见反馈{}".format(self.title)