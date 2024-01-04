from django import forms

from application.followup import models

class FollowupForm(forms.ModelForm):
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

    # 开始时间
    start_time = forms.DateTimeField(
        required=True,
        error_messages={
            'required': '开始日期不能为空',
        }
    )
    # 结束时间
    end_time = forms.DateTimeField(
        required=True,
        error_messages={
            'required': '结束日期不能为空',
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

    # ERP目标
    qty_obj_hour = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'ERP目标不能为空',
        }
    )

    # 实际产出
    qty_prod_hour = forms.IntegerField(
        required=True,
        error_messages={
            'required': '实际产出不能为空',
        }
    )

    # ERP目标累计
    cumul_qty_obj = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'ERP目标累计不能为空',
        }
    )

    # 实际累计
    cumul_qty_prod = forms.IntegerField(
        required=True,
        error_messages={
            'required': '实际累计不能为空',
        }
    )

    # 损耗工时
    loss_time = forms.IntegerField(
        required=True,
        error_messages={
            'required': '损耗工时不能为空',
        }
    )

    # 换线时间
    changeover_time = forms.IntegerField(
        required=True,
        error_messages={
            'required': '换线时间不能为空',
        }
    )

    # 问题
    problems = forms.CharField(
        required=False,
        max_length=200,
        error_messages={
            'max_length': '问题长度不得超过200个字符',
        }
    )

    # 行动
    actions = forms.CharField(
        required=False,
        max_length=200,
        error_messages={
            'max_length': '行动长度不得超过200个字符',
        }
    )

    # 备注
    remark = forms.CharField(
        required=False,
        max_length=200,
        error_messages={
            'max_length': '行动长度不得超过200个字符',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Followup
        # 指定部分字段验证
        fields = ['start_time',
                  'end_time',
                  'item_number',
                  'qty_obj_hour',
                  'qty_prod_hour',
                  'cumul_qty_obj',
                  'cumul_qty_prod',
                  'loss_time',
                  'changeover_time',
                  'problems',
                  'actions',
                  'remark',
                  'product_name']
