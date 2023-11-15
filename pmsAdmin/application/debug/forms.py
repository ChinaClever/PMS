
from django import forms

from application.debug import models


# 表单验证
class DebugForm(forms.ModelForm):
    # 下单日期
    order_time = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': '下单日期不能为空',
        }
    )
    # 客户名称
    client_name = forms.CharField(
        max_length=20,
        error_messages={
            'required': '客户名称不能为空',
            'max_length': '客户名称长度不得超过20个字符',
        }
    )
    # 规格型号
    shape = forms.CharField(
        max_length=150,
        error_messages={
            'required': '规格型号不能为空',
            'max_length': '规格型号长度不得超过150个字符',
        }
    )
    # 产品名称
    product_name = forms.CharField(
        max_length=150,
        error_messages={
            'required': '产品名称不能为空',
            'max_length': '产品名称长度不得超过150个字符',
        }
    )
    # 数量
    product_count = forms.IntegerField(
        min_value=0,
        error_messages={
            'required': '数量不能为空',
            'min_value': '数量不得小于0',
        }
    )
    # 交期
    submit_time = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': '交期不能为空',
        }
    )
    # 开始日期
    start_time = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': '开始日期不能为空',
        }
    )
    # 完成日期
    finish_time = forms.DateField(
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': '完成日期不能为空',
        }
    )
    # 所用工时
    work_hours = forms.IntegerField(
        min_value=0,
        error_messages={
            'required': '所用工时为空',
            'min_value': '所用工时不得小于0',
        }
    )
    # 具体说明
    instruction = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '具体说明长度不得超过255个字符',
        }
    )
    # 备注
    remark = forms.CharField(
        required=False,
        max_length=255,
        error_messages={
            'max_length': '备注长度不得超过255个字符',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Debug
        # 指定部分字段验证
        fields = ['order_time', 'client_name', 'shape', 'product_name', 'product_count', 'submit_time', 'start_time', 'finish_time', 'work_hours',
                  'instruction', 'remark']

