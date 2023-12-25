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

from django import forms
# 城市表单验证
from application.softwarerelease import models


class SoftwarereleaseForm(forms.ModelForm):
    # 程序名称
    name = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '程序名称不能为空',
            'max_length': '程序名称长度不得超过255个字符'
        }
    )
    # 使用产品
    products = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '使用产品不能为空',
            'max_length': '使用产品长度不得超过255个字符'
        }
    )
    # 历史版本
    history_version = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '历史版本不能为空',
            'max_length': '历史版本长度不得超过255个字符'
        }
    )
    # 当前版本
    version = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '当前版本不能为空',
            'max_length': '当前版本长度不得超过255个字符'
        }
    )
    # 修改日期
    modify_time = forms.DateTimeField(
        required=False,
        error_messages={
            'required': '修改日期不能为空',
        }
    )
    # 版本说明
    version_explain = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '版本说明不能为空',
            'max_length': '版本说明不得超过255个字符'
        }
    )
    # 此次更新
    updata = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '此次更新不能为空',
            'max_length': '此次更新不得超过255个字符'
        }
    )
    # 烧录方法
    burn_method = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '烧录方法不能为空',
            'max_length': '烧录方法不得超过255个字符'
        }
    )
    # 升级方法
    upgrade_method = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '升级方法不能为空',
            'max_length': '升级方法不得超过255个字符'
        }
    )
    # 校准方法
    calibration_method = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '校准方法不能为空',
            'max_length': '校准方法不得超过255个字符'
        }
    )
    # 用户手册
    User_Manual = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '用户手册不能为空',
            'max_length': '用户手册不得超过255个字符'
        }
    )
    # 升级原因
    upgrade_cause = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'required': '升级原因不能为空',
            'max_length': '升级原因不得超过255个字符'
        }
    )
    # 程序和文档公盘位置
    documentation_position = forms.CharField(
        required= False,
    )
    # 用户使用手册和协议公盘位置
    User_Manual_position =forms.CharField(
        required= False,
    )
    attachment = forms.FileField(
        required=False,
    )

    class Meta:
        # 绑定模型
        model = models.Softwarerelease
        # 指定部分字段验证
        fields = ['name', 'products', 'history_version', 'version', 'modify_time', 'version_explain', 'updata', 'burn_method', 'upgrade_method','calibration_method','User_Manual','upgrade_cause','documentation_position','User_Manual_position','attachment'
                  ]
