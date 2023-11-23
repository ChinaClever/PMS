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
import logging
from django.core.paginator import Paginator
from constant.constants import PAGE_LIMIT
from application.softwarerelease import forms
from application.softwarerelease.models import Softwarerelease
from utils import R, regular


# 查询客户数据列表
def SoftwarereleaseList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 分页查询
    query = Softwarerelease.objects.filter(is_delete=False)
    # 角色名称模糊筛选
    name = request.GET.get('name')
    if name:
        query = query.filter(name__contains=name)
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by('-id')
    # 分页设置
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 查询分页数据
    role_list = paginator.page(page)
    # 实例化返回对象
    result = []
    # 遍历数据源
    if len(role_list) > 0:
        for item in role_list:
            data = {
                'id': item.id,
                'name': item.name,
                'products': item.products,
                'history_version': item.history_version,
                'version': item.version ,
                'modify_time': str(item.modify_time.strftime('%Y-%m-%d ')) if item.modify_time else None,
                'version_explain': item.version_explain,
                'updata': item.updata,
                'burn_method' : item.burn_method,
                'upgrade_method': item.upgrade_method,
                'calibration_method': item.calibration_method,
                'User_Manual': item.User_Manual,
                'upgrade_cause': item.upgrade_cause,
                'documentation_position' : item.documentation_position,
                'User_Manual_position' : item.User_Manual_position,
                'create_time': str(item.create_time.strftime('%Y-%m-%d ')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d ')) if item.update_time else None,
            }
            # 加入数组对象
            result.append(data)
            # 返回结果
    return R.ok(data=result, count=count)


# 根据ID获取详情
def SoftwarereleaseDetail(softwarerelease_id):
    # 根据ID查询客户
    user = Softwarerelease.objects.filter(is_delete=False, id=softwarerelease_id).first()
    # 查询结果判空
    if not user:
        return None
    # 声明结构体
    data = {
        'id': user.id,
                'name': user.name,
                'products': user.products,
                'history_version': user.history_version,
                'version': user.version ,
                'modify_time': str(user.modify_time.strftime('%Y-%m-%d ')) if user.modify_time else None,
                'version_explain': user.version_explain,
                'updata': user.updata,
                'burn_method' : user.burn_method,
                'upgrade_method': user.upgrade_method,
                'calibration_method': user.calibration_method,
                'User_Manual': user.User_Manual,
                'upgrade_cause': user.upgrade_cause,
                'documentation_position' : user.documentation_position,
                'User_Manual_position' : user.User_Manual_position,
    }
    # 返回结果
    return data


# 添加客户
def SoftwarereleaseAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.SoftwarereleaseForm(dict_data)
    if form.is_valid():
        # 程序名称
        name = form.cleaned_data.get('name')
        # 使用产品
        products = form.cleaned_data.get('products')
        # 历史版本
        history_version = form.cleaned_data.get('history_version')
        # 当前版本
        version = form.cleaned_data.get('version')
        # 修改日期
        modify_time =  form.cleaned_data.get('modify_time')
        # 版本说明
        version_explain = form.cleaned_data.get('version_explain')
        # 此次更新
        updata = form.cleaned_data.get('updata')
        # 烧录方法
        burn_method = form.cleaned_data.get('burn_method')
        # 升级方法
        upgrade_method = form.cleaned_data.get('upgrade_method')
        # 校准方法
        calibration_method  = form.cleaned_data.get('calibration_method')
        # 用户手册
        User_Manual = form.cleaned_data.get('User_Manual')
        # 升级原因
        upgrade_cause = form.cleaned_data.get('upgrade_cause')
        # 程序和文档公盘位置
        documentation_position = form.cleaned_data.get('documentation_position')
        # 用户使用手册和协议公盘位置
        User_Manual_position = form.cleaned_data.get('User_Manual_position')
        # 创建数据
        Softwarerelease.objects.create(
            name=name,
            products= products,
            history_version=history_version,
            version=version,
            modify_time=modify_time,
            version_explain=version_explain,
            updata=updata,
            burn_method=burn_method,
            upgrade_method=upgrade_method,
            calibration_method=calibration_method,
            User_Manual=User_Manual,
            upgrade_cause=upgrade_cause,
            documentation_position=documentation_position,
            User_Manual_position= User_Manual_position
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)


# 更新客户
def SoftwarereleaseUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 客户ID
        softwarerelease_id = dict_data.get('id')
        # 客户ID判空
        if not softwarerelease_id or int(softwarerelease_id) <= 0:
            return R.failed("客户ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.SoftwarereleaseForm(dict_data)
    if form.is_valid():
        # 程序名称
        name = form.cleaned_data.get('name')
        # 使用产品
        products = form.cleaned_data.get('products')
        # 历史版本
        history_version = form.cleaned_data.get('history_version')
        # 当前版本
        version = form.cleaned_data.get('version')
        # 修改日期
        modify_time = form.cleaned_data.get('modify_time')
        # 版本说明
        version_explain = form.cleaned_data.get('version_explain')
        # 此次更新
        updata = form.cleaned_data.get('updata')
        # 烧录方法
        burn_method = form.cleaned_data.get('burn_method')
        # 升级方法
        upgrade_method = form.cleaned_data.get('upgrade_method')
        # 校准方法
        calibration_method = form.cleaned_data.get('calibration_method')
        # 用户手册
        User_Manual = form.cleaned_data.get('User_Manual')
        # 升级原因
        upgrade_cause = form.cleaned_data.get('upgrade_cause')
        # 程序和文档公盘位置
        documentation_position = form.cleaned_data.get('documentation_position')
        # 用户使用手册和协议公盘位置
        User_Manual_position = form.cleaned_data.get('User_Manual_position')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询客户
    user = Softwarerelease.objects.only('id').filter(id=softwarerelease_id, is_delete=False).first()
    # 查询结果判断
    if not user:
        return R.failed("客户不存在")

    # 对象赋值
    user.name = name
    user.products = products
    user.history_version = history_version
    user.version = version
    user.modify_time = modify_time
    user.version_explain = version_explain
    user.updata = updata
    user.burn_method = burn_method
    user.upgrade_method = upgrade_method
    user.calibration_method = calibration_method
    user.User_Manual = User_Manual
    user.upgrade_cause = upgrade_cause
    user.documentation_position = documentation_position
    user.User_Manual_position = User_Manual_position
    print(user.documentation_position)
    print('------------')

    # 更新数据
    user.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除客户
def SoftwarereleaseDelete(softwarerelease_id):
    # 记录ID为空判断
    if not softwarerelease_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = softwarerelease_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            user = Softwarerelease.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not user:
                return R.failed("不存在")
            # 设置删除标识
            user.is_delete = True
            # 更新记录
            user.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))
