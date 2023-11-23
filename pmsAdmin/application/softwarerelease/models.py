# +----------------------------------------------------------------------
# | DjangoAdmin敏捷开发框架 [ 赋能开发者，助力企业发展 ]
# +----------------------------------------------------------------------
# | 版权所有 2021~2023 北京DjangoAdmin研发中心
# +----------------------------------------------------------------------
# | Licensed LGPL-3.0 DjangoAdmin并不是自由软件，未经许可禁止去掉相关版权
# +----------------------------------------------------------------------
# | 官方网站: https://www.djangoadmin.cn
# +----------------------------------------------------------------------
# | 作者: @一米阳光 团队荣誉出品
# +----------------------------------------------------------------------
# | 版权和免责声明:
# | 本团队对该软件框架产品拥有知识产权（包括但不限于商标权、专利权、著作权、商业秘密等）
# | 均受到相关法律法规的保护，任何个人、组织和单位不得在未经本团队书面授权的情况下对所授权
# | 软件框架产品本身申请相关的知识产权，禁止用于任何违法、侵害他人合法权益等恶意的行为，禁
# | 止用于任何违反我国法律法规的一切项目研发，任何个人、组织和单位用于项目研发而产生的任何
# | 意外、疏忽、合约毁坏、诽谤、版权或知识产权侵犯及其造成的损失 (包括但不限于直接、间接、
# | 附带或衍生的损失等)，本团队不承担任何法律责任，本软件框架禁止任何单位和个人、组织用于
# | 任何违法、侵害他人合法利益等恶意的行为，如有发现违规、违法的犯罪行为，本团队将无条件配
# | 合公安机关调查取证同时保留一切以法律手段起诉的权利，本软件框架只能用于公司和个人内部的
# | 法律所允许的合法合规的软件产品研发，详细声明内容请阅读《框架免责声明》附件；
# +----------------------------------------------------------------------

from django.db import models

# Create your models here.
from application.models import BaseModel

from config.env import TABLE_PREFIX


# 烧录表格
class Softwarerelease(BaseModel):
    # 程序名称
    name = models.CharField(null=False, max_length=6, verbose_name="程序名称", help_text="程序名称")
    # 使用产品
    products = models.CharField(null=False, max_length=20, verbose_name="使用产品", help_text="使用产品")
    # 历史版本
    history_version = models.CharField(null=True, max_length=20, verbose_name="历史版本", help_text="历史版本")
    # 当前版本
    version = models.CharField(null=False, max_length=6, verbose_name="当前版本", help_text="当前版本")
    # 修改日期
    modify_time = models.DateTimeField(null=False, max_length=18, verbose_name="修改日期", help_text="修改日期")
    # 版本说明
    version_explain = models.CharField(null=True, max_length=18, verbose_name="版本说明", help_text="版本说明")
    # 此次更新
    updata = models.CharField(null=True, max_length=150,verbose_name="此次更新", help_text="此次更新")
    # 烧录方法
    burn_method = models.CharField(null=True,max_length=150, verbose_name="烧录方法", help_text="烧录方法")
    # 升级方法
    upgrade_method = models.CharField(null=True, max_length=150, verbose_name="升级方法", help_text="升级方法")
    # 校准方法
    calibration_method = models.CharField(null=True, max_length=150, verbose_name="校准方法", help_text="校准方法")
    # 用户手册
    User_Manual = models.CharField(null=True, max_length=150, verbose_name="用户手册", help_text="用户手册")
    # 升级原因
    upgrade_cause = models.CharField(null=True, max_length=150, verbose_name="升级原因", help_text="升级原因")
    # 程序和文档公盘位置
    documentation_position = models.CharField(null=True, max_length=150, verbose_name="程序和文档公盘位置", help_text="程序和文档公盘位置")
    # 用户使用手册和协议公盘位置
    User_Manual_position = models.CharField(null=True, max_length=150, verbose_name="用户使用手册和协议公盘位置", help_text="用户使用手册和协议公盘位置")
    class Meta:
        # 数据表名
        db_table = TABLE_PREFIX + "softwarerelease"
        verbose_name = ("出厂报告表")
        verbose_name_plural = verbose_name

    def __str__(self):
        return '程序名{}'.format(self.id)