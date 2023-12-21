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
# 客户表单验证
from application.burning import models


class BurningForm(forms.ModelForm):
    # 客户名称
    work_order = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '工单号不能为空',
            'max_length': '工单号不得超过255个字符'
        }
    )
    name = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '客户名称不能为空',
            'max_length': '客户名称长度不得超过255个字符'
        }
    )
    # 规格型号
    code = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '规格型号不能为空',
            'max_length': '规格型号长度不得超过255个字符'
        }
    )
    # 版本号
    version = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '版本号不能为空',
            'max_length': '版本号长度不得超过255个字符'
        }
    )
    # 程序要求
    require = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '程序要求不能为空',
            'max_length': '程序要求不得超过255个字符'
        }
    )
    # 订单日期
    order_time = forms.DateTimeField(
        # max_length=18,
        error_messages={
            'required': '订单日期不能为空',
        }
    )
    # 交货日期
    delivery_time = forms.DateTimeField(
        error_messages={
            'required': '交货日期不能为空',
        }
    )

    #  订单数量
    quantity= forms.IntegerField(
        required=True,
        error_messages={
            'required': '数量不能为空',
        }
    )
    print(type(quantity))
    # 备注
    remark = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '备注长度不得超过255个字符'
        }
    )
    # rcerder
    rcerder = forms.CharField(
        required=True,
        max_length=255,
        error_messages={
            'required': '备注不能为空',
            'max_length': '备注长度不得超过255个字符'
        }
    )
    # 烧录数量
    burning_quantity = forms.IntegerField(
        required=True,
        error_messages={
            'required': '数量不能为空',
        }
    )
    # 开始日期
    start_time = forms.DateTimeField(
        error_messages={
            'required': '交货日期不能为空',
        }
    )
    # 完成日期
    finish_time = forms.DateTimeField(
        error_messages={
            'required': '交货日期不能为空',
        }
    )
    # 工时
    work_hours = forms.IntegerField(
        required=True,
        error_messages={
            'required': '数量不能为空',
        }
    )
    class Meta:
        # 绑定模型
        model = models.burning
        # 指定部分字段验证
        fields = ['work_order','name', 'code', 'version', 'require', 'order_time', 'delivery_time', 'quantity', 'remark', 'rcerder','burning_quantity','start_time','finish_time','work_hours',
                  ]
