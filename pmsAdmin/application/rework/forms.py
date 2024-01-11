from django import forms

from application.rework import models

class ReworkForm(forms.ModelForm):
    # 工单号
    work_order = forms.CharField(
        required=True,
        error_messages={
            'required': '工单号不能为空',
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

    product_module = forms.IntegerField(
        required=True,
        error_messages={
            'required': '成品/模块不能为空',
        }
    )

    # 产品型号
    item_number = forms.CharField(
        required=True,
        max_length=40,
        error_messages={
            'required': '产品型号不能为空',
            'max_length': '产品型号长度不得超过40个字符',
        }
    )
    # 返工数量
    rw_qty = forms.IntegerField(
        required=True,
        error_messages={
            'required': '返工数量不能为空',
        }
    )

    # 返工原因
    rw_reason = forms.IntegerField(
        required=True,
        error_messages={
            'required': '返工原因不能为空',
        }
    )

    # 损耗工时
    loss_time = forms.IntegerField(
        required=True,
        error_messages={
            'required': '损耗工时不能为空',
        }
    )

    # 损耗材料数量
    loss_material_qty = forms.IntegerField(
        required=True,
        error_messages={
            'required': '损耗材料数量不能为空',
        }
    )

    # 损耗材料名称
    loss_material_name = forms.CharField(
        required=True,
        max_length=200,
        error_messages={
            'required': '损耗材料名称不能为空',
            'max_length': '损耗材料名称长度不得超过200个字符',
        }
    )

    # 责任归属人
    respon = forms.CharField(
        required=True,
        max_length=200,
        error_messages={
            'required': '责任归属人不能为空',
            'max_length': '责任归属人长度不得超过200个字符',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Rework
        # 指定部分字段验证
        fields = ['work_order',
                  'item_number',
                  'rw_qty',
                  'loss_time',
                  'loss_material_qty',
                  'loss_material_name',
                  'respon',
                  'rw_reason',
                  'product_name']
