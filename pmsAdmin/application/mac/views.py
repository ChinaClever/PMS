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

from django.http import HttpResponse
from django.shortcuts import render
from application.shipmentreport.models import Shipment
# Create your views here.

from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect,reverse
from application.mac import services
from application.constants import CITY_LEVEL_LIST
from application.mac.models import mac

from config.env import DEBUG
from middleware.login_middleware import check_login
from middleware.permission_middleware import PermissionRequired

from utils import R


# 查询分页数据
@method_decorator(check_login, name='get')
class MacListView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:mac:list',)

    # 接收GET请求
    def get(self, request):
        # 调用查询分页数据
        result = services.MacList(request)
        # 返回结果
        return result


# 查询数据
@method_decorator(check_login, name='get')
class MacDetailView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:mac:detail',)

    # 接收GET请求
    def get(self, request, mac_id):
        # 调用查询方法
        data = services.MacDetail(mac_id)
        # 返回结果
        return R.ok(data=data)


# 添加
@method_decorator(check_login, name='post')
class MacAddView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:mac:add',)

    # 接收POST请求
    def post(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用添加方法
        result = services.MacAdd(request)
        # 返回结果
        return result


# 更新
@method_decorator(check_login, name='put')
class MacUpdateView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:mac:update',)

    # 接收PUT请求
    def put(self, request):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用更新方法
        result = services.MacUpdate(request)
        # 返回结果
        return result


# 删除
@method_decorator(check_login, name='delete')
class MacDeleteView(PermissionRequired, View):
    # 方法权限标识
    permission_required = ('sys:mac:delete',)

    # 接收delete请求
    def delete(self, request, mac_id):
        if DEBUG:
            return R.failed("演示环境，暂无操作权限")
        # 调用删除方法
        result = services.MacDelete(mac_id)
        # 返回结果
        return result


# 定义 MAC 地址初始值
mac_suffix = 0

def test(request):
    global mac_suffix  # 声明为全局变量
    objs = mac.objects.all()
    if objs:
        last_row = mac.objects.filter(is_delete=0).latest('id')
        original_mac = last_row.mac_address
        # 将原始 MAC 地址转换为十进制整数，并增加1
        new_mac_int = (int(original_mac.replace(':', ''), 16) + 1) % (256 ** 6)
        # 将新的值转换为十六进制字符串，并保持12位长度
        new_mac_str = hex(new_mac_int)[2:].zfill(12)
        # 在每两位字符之间加上冒号并生成新的 MAC 地址
        new_mac = ':'.join([new_mac_str[i:i + 2] for i in range(0, len(new_mac_str), 2)])
        # 连接每个部分并生成新的 MAC 地址
        mac_id = new_mac
    else:
        # 将 MAC 地址后缀转换为十六进制字符串
        mac_hex = hex(mac_suffix)[2:].zfill(12)
        # 拼接 MAC 地址
        mac_id = f"{mac_hex[0:2]}:{mac_hex[2:4]}:{mac_hex[4:6]}:{mac_hex[6:8]}:{mac_hex[8:10]}:{mac_hex[10:12]}"

    work_order = request.GET.get('work_order')
    try:
        shipment = Shipment.objects.filter(work_order=work_order).first()
        if shipment==None:
            return HttpResponse('排期表单没有该工单号')
        else:
            name = shipment.client_name
            code = shipment.shape
    except Shipment.DoesNotExist:
        return HttpResponse('排期表单没有该工单号')

    serial_id = request.GET.get('serial_id')
    mac_address = mac_id

    # 创建数据库对象
    obj = mac(work_order=work_order, name=name,code=code, serial_id=serial_id, mac_address=mac_address)
    # 保存对象到数据库
    obj.save()

    response_data = {'mac_address': mac_address}
    # 增加 MAC 地址后缀
    mac_suffix += 1
    return HttpResponse(json.dumps(response_data))
#http://localhost:8000/mac/test?work_order=12345&serial_id=12345
