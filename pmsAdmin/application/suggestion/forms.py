from django import forms

from application.suggestion import models

class SuggestionForm(forms.ModelForm):
    # 提交人
    commit_user = forms.CharField(
        required=False,
        max_length=20,
        error_messages={
            'max_length': '提交人长度不得超过20个字符',
        }
    )
    # 类型：1-问题 2-建议 3-新需求
    type = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=3,
        error_messages={
            'required': '类型不能为空',
            'min_value': '类型值在1~3之间',
            'max_value': '类型值在1~3之间',
        }
    )

    # 处理状态：1-未查看 2-确认 3-完成 4-未通过
    status = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=4,
        error_messages={
            'required': '状态不能为空',
            'min_value': '状态值在1~4之间',
            'max_value': '状态值在1~4之间',
        }
    )

    # 优先级(1-10)
    priority = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=10,
        error_messages={
            'required': '状态不能为空',
            'min_value': '状态值在1~10之间',
            'max_value': '状态值在1~10之间',
        }
    )

    # 通知公告内容
    content = forms.CharField(
        required=True,
        max_length=200,
        error_messages={
            'required': '内容不能为空',
            'max_length': '内容长度不得超过200个字符',
        }
    )

    feedback = forms.CharField(
        required=False,
        max_length=200,
        error_messages={
            'required': '反馈不能为空',
            'max_length': '内容长度不得超过200个字符',
        }
    )

    class Meta:
        # 绑定模型
        model = models.Suggestion
        # 指定部分字段验证
        fields = ['commit_user', 'type', 'status', 'priority', 'content','feedback']
