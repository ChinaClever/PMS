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
from datetime import datetime

from django.shortcuts import render
import json
# Create your views here.

from django.utils.decorators import method_decorator
from django.views import View

from application.burning import services
from application.burning.models import burning
from application.constants import CITY_LEVEL_LIST
from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

from utils import R


# 查询分页数据
@method_decorator(check_login, name='get')
class BurningListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:burning:list',)

    # 接收GET请求
    def get(self, request):
        # 调用查询分页数据
        result = services.BurningList(request)
        # 返回结果
        return result


# 查询数据
@method_decorator(check_login, name='get')
class BurningDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:burning:detail',)

    # 接收GET请求
    def get(self, request, burning_id):
        # 调用查询方法
        data = services.BurningDetail(burning_id)
        # 返回结果
        return R.ok(data=data)


# 添加
@method_decorator(check_login, name='post')
class BurningAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:burning:add',)

    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加方法
        result = services.BurningAdd(request)
        # 返回结果
        return result


# 更新
@method_decorator(check_login, name='put')
class BurningUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:burning:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新方法
        result = services.BurningUpdate(request)
        # 返回结果
        return result


# 删除
@method_decorator(check_login, name='delete')
class BurningDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:burning:delete',)

    # 接收delete请求
    def delete(self, request, burning_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除方法
        result = services.BurningDelete(burning_id)
        # 返回结果
        return result



# 批量添加
def adds(request):
    # 接收请求参数
    json_data = request.body.decode()
    # 参数为空判断
    if not json_data:
        return R.failed("参数不能为空")
    # 数据类型转换
    dict_data = json.loads(json_data)
    print(dict_data)
    # 获取数据
    # 工单号
    work_order = dict_data.get('work_order')
    # pcb信息
    information = dict_data.get('times')
    time1 = ''
    time2 = ''
    time3 = ''
    for i in range(len(information)-1):
        if i == len(information)-2:
            time1 += information[i]
        else:
            time1 += information[i]
            time1 += ','
    for i in range(1,len(information)):
        if i == len(information) - 1:
            time2 += information[i]
        else:
            time2 += information[i]
            time2 += ','
    # 转换
    time4 = time1.split(',')
    time5 = time2.split(',')
    for i in range(len(time4)):
        if i == len(time4)-1:
            time4[i] = datetime.strptime(time4[i] , "%Y/%m/%d %H:%M:%S")
            time5[i] = datetime.strptime(time5[i] , "%Y/%m/%d %H:%M:%S")
            a = round((time5[i] - time4[i]).total_seconds()/60/60,6)
            time3 += str(a)
        else:
            time4[i] = datetime.strptime(time4[i], "%Y/%m/%d %H:%M:%S")
            time5[i] = datetime.strptime(time5[i], "%Y/%m/%d %H:%M:%S")
            a = round((time5[i] - time4[i]).total_seconds() / 3600,6)
            time3 += str(a)
            time3 += ','
    # 客户名称
    name = dict_data.get('name')
    # 规格型号
    code = dict_data.get('code')
    # 版本号
    version = dict_data.get('version')
    # 程序要求
    require = dict_data.get('require')
    # 订单日期
    order_time = dict_data.get('order_time')
    # 交货日期
    delivery_time = dict_data.get('delivery_time')
    # 数量
    quantity = dict_data.get('quantity')
    # 备注
    remark = dict_data.get('remark')
    # rxerder
    rcerder = dict_data.get('rcerder')
    # 烧录数量
    burning_quantity = len(information)-1
    PCB_code = dict_data.get('PCB_code')
    start_time = time1.replace("/", "-")
    finish_time = time2.replace("/", "-")
    work_hours = time3

    # 创建数据
    burning.objects.create(
        work_order=work_order,
        PCB_code=PCB_code,
        name=name,
        code=code,
        version=version,
        require=require,
        order_time=order_time,
        delivery_time=delivery_time,
        quantity=quantity,
        remark=remark,
        rcerder=rcerder,
        burning_quantity=burning_quantity,
        start_time=start_time,
        finish_time=finish_time,
        work_hours=work_hours,
    )
    # 返回结果
    return R.ok(msg="创建成功")

