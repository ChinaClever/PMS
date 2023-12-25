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
import os
import uuid
import logging
from datetime import datetime

from django.core.paginator import Paginator
from constant.constants import PAGE_LIMIT
from application.softwarerelease.models import Softwarerelease
from utils import R, regular


# 查询客户数据列表
def SoftwarereleaseList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = request.GET.get('limit')
    if limit:
        limit = int(request.GET.get('limit'))
    else:
        limit = 65535000;
    # 分页查询
    query = Softwarerelease.objects.filter(is_delete=False)
    # 角色名称模糊筛选
    name = request.GET.get('name')
    if name:
        query = query.filter(name__contains=name)
        # 筛选年月范围
    selectStartDate = request.GET.get('selectStartDate')
    selectEndDate = request.GET.get('selectEndDate')
    if selectStartDate and selectEndDate:
        start_date = datetime.strptime(selectStartDate, "%Y-%m-%d")
        end_date = datetime.strptime(selectEndDate, "%Y-%m-%d")
        query = query.filter(modify_time__gte=start_date, modify_time__lte=end_date)

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
                'name': item.name if item.name else None,
                'products': item.products if item.products else None,
                'history_version': item.history_version if item.history_version else None,
                'version': item.version  if item.version else None,
                'modify_time': str(item.modify_time.strftime('%Y-%m-%d ')) if item.modify_time else None,
                'version_explain': item.version_explain if item.version_explain else None,
                'updata': item.updata if item.updata else None,
                'burn_method' : item.burn_method if item.burn_method else None,
                'upgrade_method': item.upgrade_method if item.upgrade_method else None,
                'calibration_method': item.calibration_method if item.calibration_method else None,
                'User_Manual': item.User_Manual if item.User_Manual else None,
                'upgrade_cause': item.upgrade_cause if item.upgrade_cause else None,
                'documentation_position' : item.documentation_position if item.documentation_position else None,
                'User_Manual_position' : item.User_Manual_position if item.User_Manual_position else None,
                'attachment': item.attachment if item.attachment else None,
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
                'name': user.name if user.name else None,
                'products': user.products if user.products else None,
                'history_version': user.history_version if user.history_version else None,
                'version': user.version if user.version else None,
                'modify_time': str(user.modify_time.strftime('%Y-%m-%d ')) if user.modify_time else None,
                'version_explain': user.version_explain if user.version_explain else None,
                'updata': user.updata if user.updata else None,
                'burn_method' : user.burn_method if user.burn_method else None,
                'upgrade_method': user.upgrade_method if user.upgrade_method else None,
                'calibration_method': user.calibration_method if user.calibration_method else None,
                'User_Manual': user.User_Manual if user.User_Manual else None,
                'upgrade_cause': user.upgrade_cause if user.upgrade_cause else None,
                'documentation_position' : user.documentation_position if user.documentation_position else None,
                'User_Manual_position' : user.User_Manual_position if user.User_Manual_position else None,
                'attachment':'attachment' if user.attachment else None,
    }
    # 返回结果
    return data


# 添加客户
def SoftwarereleaseAdd(request):

    # 程序名称
    name = request.POST.get('name')
    # 使用产品
    products = request.POST.get('products')
    # 历史版本
    history_version = request.POST.get('history_version')
    # 当前版本
    version = request.POST.get('version')
    # 修改日期
    modify_time =  request.POST.get('modify_time')

    # 版本说明
    version_explain = request.POST.get('version_explain')
    # 此次更新
    updata = request.POST.get('updata')
    # 烧录方法
    burn_method = request.POST.get('burn_method')
    # 升级方法
    upgrade_method = request.POST.get('upgrade_method')
    # 校准方法
    calibration_method  = request.POST.get('calibration_method')
    # 用户手册
    User_Manual = request.POST.get('User_Manual')
    # 升级原因
    upgrade_cause = request.POST.get('upgrade_cause')
    # 程序和文档公盘位置
    documentation_position = request.POST.get('documentation_position')
    # 用户使用手册和协议公盘位置
    User_Manual_position = request.POST.get('User_Manual_position')


    FileSavePath = "public/uploads/softwarerelease"
    files = request.FILES.getlist('files')
    # 存储文件路径和名称的列表字符串
    attachmentListToString = []
    if files:
        # 存储文件路径和名称的列表
        attachment_list = []
        for file in files:
            # 生成唯一的文件名
            unique_filename = str(uuid.uuid4()) + '_' + file.name
            # 构建文件的完整保存路径
            save_path = os.path.join(FileSavePath, unique_filename)
            # 数据库存的去掉"public/" 方便前端调用
            save_path1 = save_path.replace("public/", "")
            # 确保目标文件夹存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # 将文件保存到服务器
            with open(save_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # 将文件路径和名称添加到列表中
            attachment_list.append(save_path1)
            # 将文件路径和名称列表转换为字符串，使用逗号分隔
        attachmentListToString = ','.join(attachment_list)
        print(attachmentListToString)

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
        User_Manual_position= User_Manual_position,
        attachment = attachmentListToString if files else None,
    )
    # 返回结果
    return R.ok(msg="创建成功")



# 更新客户
def SoftwarereleaseUpdate(request):
    # ID
    softwarerelease_id = request.POST.get('id')
    # ID判空
    if not softwarerelease_id or int(softwarerelease_id) <= 0:
        return R.failed("ID不能为空")
    # 根据ID查询
    softwarerelease = Softwarerelease.objects.only('id').filter(id=softwarerelease_id, is_delete=False).first()
    # 查询结果判断
    if not softwarerelease:
        return R.failed("数据不存在,请重试！")
    FileSavePath = "public/uploads/softwarerelease"
    files = request.FILES.getlist('files')
    # 存储文件路径和名称的列表
    attachment_list = []
    if files:
        for file in files:
            # 生成唯一的文件名
            unique_filename = str(uuid.uuid4()) + '_' + file.name
            # 构建文件的完整保存路径
            save_path = os.path.join(FileSavePath, unique_filename)
            # 数据库存的去掉"public/" 方便前端调用
            save_path1 = save_path.replace("public/", "")
            # 确保目标文件夹存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # 将文件保存到服务器
            with open(save_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # 将文件路径和名称添加到列表中
            attachment_list.append(save_path1)

    # 程序名称
    name = request.POST.get('name')
    # 使用产品
    products = request.POST.get('products')
    # 历史版本
    history_version = request.POST.get('history_version')
    # 当前版本
    version = request.POST.get('version')
    # 修改日期
    modify_time = request.POST.get('modify_time')
    modify_time = datetime.strptime(modify_time, '%Y-%m-%d')
    # 版本说明
    version_explain = request.POST.get('version_explain')
    # 此次更新
    updata = request.POST.get('updata')
    # 烧录方法
    burn_method = request.POST.get('burn_method')
    # 升级方法
    upgrade_method = request.POST.get('upgrade_method')
    # 校准方法
    calibration_method = request.POST.get('calibration_method')
    # 用户手册
    User_Manual = request.POST.get('User_Manual')
    # 升级原因
    upgrade_cause = request.POST.get('upgrade_cause')
    # 程序和文档公盘位置
    documentation_position = request.POST.get('documentation_position')
    # 用户使用手册和协议公盘位置
    User_Manual_position = request.POST.get('User_Manual_position')


    # 日期格式转化
    if modify_time == "null":
        modify_time = ""

    # 删除文件
    deleteFileList = request.POST.get('deleteFileList')
    # 使用逗号分割字符串，得到文件路径列表
    file_paths = softwarerelease.attachment.split(',') if softwarerelease.attachment else []

    if deleteFileList:

        for index, file_name in enumerate(file_paths):
            # 存在deleteFileList列表中 表示要删除
            if file_name in deleteFileList:
                delete_file_path = 'public/' + file_paths[index]
                try:
                    os.remove(delete_file_path)
                    print(delete_file_path + "文件删除成功")
                except OSError as e:
                    print(f"文件删除失败: {e}")
            # 不用删除的添加进attachment_list 后续加入数据库
            else:
                attachment_list.append(file_paths[index])
    # 没有删除文件的时候 原本的路径全添加进attachment_list
    else:
        attachment_list += file_paths

    if attachment_list:
        # 将文件路径和名称列表转换为一个字符串，使用逗号分隔
        attachmentListToString = ','.join(attachment_list)
        # 没有attachment_list 有deleteFileList表示删除全部
    elif deleteFileList:
        attachmentListToString = ''
    else:
        # 没有attachment_list和deleteFileList表示没有对附件操作
        attachmentListToString = softwarerelease.attachment



    # 根据ID查询客户
    user = Softwarerelease.objects.only('id').filter(id=softwarerelease_id, is_delete=False).first()
    # 查询结果判断
    if not user:
        return R.failed("客户不存在")
    current_time = datetime.now()
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
    user.update_time = current_time
    user.attachment = attachmentListToString

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
