from django import forms

from application.inspectreport import models

class InspectreportForm(forms.ModelForm):
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
    # 检验数量
    examine_an_amount = forms.IntegerField(
        required=True,
        error_messages={
            'required': '检验数量不能为空',
        }
    )

    # 检验不良数量
    examine_a_bad_amount = forms.IntegerField(
        required=True,
        error_messages={
            'required': '检验不良数量不能为空',
        }
    )

    # 检验数量累计
    examine_amount_total_amount = forms.IntegerField(
        required=True,
        error_messages={
            'required': '检验数量累计不能为空',
        }
    )

    # 检验不良累计
    examine_bad_total_amount = forms.IntegerField(
        required=True,
        error_messages={
            'required': '检验不良累计不能为空',
        }
    )

    # ERP目标合格率
    target_pass_rate = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=100,
        error_messages={
            'min_value': 'ERP目标合格率在0~100之间',
            'max_value': 'ERP目标合格率在0~100之间',
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

    class Meta:
        # 绑定模型
        model = models.Inspectreport
        # 指定部分字段验证
        fields = ['start_time',
                  'end_time',
                  'item_number',
                  'examine_an_amount',
                  'examine_a_bad_amount',
                  'examine_amount_total_amount',
                  'examine_bad_total_amount',
                  'target_pass_rate',
                  'problems',
                  'actions',
                  'product_name']
