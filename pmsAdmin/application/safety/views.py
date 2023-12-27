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
import json
import math

import numpy as np
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect,reverse
from application.safety import services
from application.constants import CITY_LEVEL_LIST
from application.safety.models import safety

from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

from utils import R


# 查询分页数据
@method_decorator(check_login, name='get')
class SafetyListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:safety:list',)

    # 接收GET请求
    def get(self, request):
        # 调用查询分页数据
        result = services.SafetyList(request)
        # 返回结果
        return result


# 查询数据
@method_decorator(check_login, name='get')
class SafetyDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:safety:detail',)

    # 接收GET请求
    def get(self, request, safety_id):
        # 调用查询方法
        data = services.SafetyDetail(safety_id)
        # 返回结果
        return R.ok(data=data)


# 添加

class SafetyAddView(View):
    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加方法
        result = services.SafetyAdd(request)
        # 返回结果
        return result


# 更新
@method_decorator(check_login, name='put')
class SafetyUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:safety:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新方法
        result = services.SafetyUpdate(request)
        # 返回结果
        return result


# 删除
@method_decorator(check_login, name='delete')
class SafetyDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:safety:delete',)

    # 接收delete请求
    def delete(self, request, safety_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除方法
        result = services.SafetyDelete(safety_id)
        # 返回结果
        return result

# 导入文件
def upload(request):
    a = [] #存储信息
    file = request.FILES['file']
    # 使用 pandas 读取文件数据
    df = pd.read_excel(file)
    # 获取行数
    num_rows = df.shape[0]
    for i in range(num_rows):
        # 获取每一行结果
        row_data = df.iloc[num_rows-1-i]
        for j in row_data:
            a.append(j)
        a = [elem if not pd.isnull(elem) else None for elem in a]
        # 创建数据库对象
        try :
            obj = safety(work_order=a[0], softwareType=a[1], productType=a[2], productSN=a[3], Gnd=a[4],Ir=a[5],Dcw=a[6],Acw=a[7],result=a[8],softwareVersion=a[9],companyName=a[10],protocolVersion=a[11],testStartTime=a[12],testEndTime=a[13],testTime=a[14],create_time=a[15],update_time=a[16])
            # 保存对象到数据库
            obj.save()
            a.clear()
            return R.ok('添加成功')
        except:
            a.clear()
            return R.failed('请确保格式正确，时间是年月日时分秒')
    return HttpResponse('测试成功')

