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
from datetime import datetime#改时间格式
from application.supplier import forms
from application.supplier.models import Dict
from constant.constants import PAGE_LIMIT
from utils import R, regular

# 查询字典分页数据
from utils.utils import uid



def DictList(request):#查询设置，从前端返回order_id字段，再到数据库中去查询相应字段，排序后返回给前端
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Dict.objects.filter(is_delete=False)
    # 字典名称模糊筛选
    work_order = request.GET.get('work_order')#前端返回的字段
    if work_order:
        query = query.filter(work_order__contains=work_order)
    #时间筛选
    selectStartDate = request.GET.get('selectStartDate')
    selectEndDate = request.GET.get('selectEndDate')
    if selectStartDate and selectEndDate:
        start_date = datetime.strptime(selectStartDate, "%Y-%m-%d")
        end_date = datetime.strptime(selectEndDate, "%Y-%m-%d")
        query = query.filter(create_time__date_gte=start_date, create_time__date_lte=end_date)
    # 排序
    #query = query.order_by("-id")
    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by("-id")
    # 设置分页
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    dict_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(dict_list) > 0:
        '''for item in dict_list:
            data = {
                'id': item.id,
                'name': item.name,
                'code': item.code,
                'sort': item.sort,
                'note': item.note,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }
            
            result.append(data)'''
        for item in dict_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'customer': item.customer,
                'product_name': item.product_name,
                'product_type': item.product_type,
                'supplier': item.supplier,
                'parts': item.parts,
                'product_number': item.product_number,
                'notes': item.notes,
                'create_time': str(item.create_time.strftime('%Y-%m-%d %H:%M:%S')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d %H:%M:%S')) if item.update_time else None,
            }

            result.append(data)

    # 返回结果
    return R.ok(data=result, count=count)


# 根据ID查询字典
def DictDetail(dict_id):
    # 根据ID查询字典
    dict = Dict.objects.filter(is_delete=False, id=dict_id).first()
    # 查询结果判空
    if not dict:
        return None
    # 声明结构体
    '''data = {
        'id': dict.id,
        'name': dict.name,
        'code': dict.code,
        'sort': dict.sort,
        'note': dict.note,
    }'''
    data = {
        'id': dict.id,
        'work_order': dict.work_order,
        'customer': dict.customer,
        'product_name': dict.product_name,
        'product_type': dict.product_type,
        'supplier': dict.supplier,
        'parts': dict.parts,
        'product_number':dict.product_number,
        'notes': dict.notes,
    }
    # 返回结果
    return data


# 添加字典
def DictAdd(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # goods = Dict.objects.filter(work_order=dict_data.get('work_order')).first()
        # if goods:
        #     return R.failed("工单号已存在")

    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.DictForm(dict_data)
    if form.is_valid():
        # 字典名称
        #name = form.cleaned_data.get('name')
        # 字典编码
        #code = form.cleaned_data.get('code')
        # 字典排序
        #sort = form.cleaned_data.get('sort')
        # 字典备注
        #note = form.cleaned_data.get('note')
        work_order = form.cleaned_data.get('work_order')
        customer = form.cleaned_data.get('customer')
        product_name = form.cleaned_data.get('product_name')
        product_type = form.cleaned_data.get('product_type')
        supplier = form.cleaned_data.get('supplier')
        parts = form.cleaned_data.get('parts')
        product_number = form.cleaned_data.get('product_number')
        notes = form.cleaned_data.get('notes')
        # 创建数据
        Dict.objects.create(
            #name=name,
            #code=code,
            #sort=sort,
            #note=note,
            work_order=work_order,
            customer=customer,
            product_name=product_name,
            product_type=product_type,
            supplier=supplier,
            parts=parts,
            product_number=product_number,
            notes=notes,
            create_user=uid(request)
        )
        # 返回结果
        return R.ok(msg="创建成功")
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)


# 更新字典
def DictUpdate(request):
    try:
        # 接收请求参数
        json_data = request.body.decode()
        # 参数为空判断
        if not json_data:
            return R.failed("参数不能为空")
        # 数据类型转换
        dict_data = json.loads(json_data)
        # 字典ID
        dict_id = dict_data.get('id')
        # 字典ID判空
        if not dict_id or int(dict_id) <= 0:
            return R.failed("ID不能为空")
    except Exception as e:
        logging.info("错误信息：\n{}", format(e))
        return R.failed("参数错误")
    # 表单验证
    form = forms.DictForm(dict_data)
    if form.is_valid():
        # 字典名称
        #name = form.cleaned_data.get('name')
        # 字典编码
        #code = form.cleaned_data.get('code')
        # 字典排序
        #sort = form.cleaned_data.get('sort')
        # 字典备注
        #note = form.cleaned_data.get('note')
        work_order = form.cleaned_data.get('work_order')
        customer = form.cleaned_data.get('customer')
        product_name = form.cleaned_data.get('product_name')
        product_type = form.cleaned_data.get('product_type')
        supplier = form.cleaned_data.get('supplier')
        parts = form.cleaned_data.get('parts')
        product_number = form.cleaned_data.get('product_number')
        notes = form.cleaned_data.get('notes')
        update_time = form.cleaned_data.get('update_time')
    else:
        # 获取错误信息
        err_msg = regular.get_err(form)
        # 返回错误信息
        return R.failed(err_msg)

    # 根据ID查询字典
    dict = Dict.objects.only('id').filter(id=dict_id, is_delete=False).first()
    # 查询结果判断
    if not dict:
        return R.failed("字典不存在")

    # 对象赋值
    '''dict.name = name
    dict.code = code
    dict.sort = sort
    dict.note = note'''
    dict.work_order = work_order
    dict.customer = customer
    dict.product_name = product_name
    dict.product_type = product_type
    dict.supplier = supplier
    dict.parts = parts
    dict.product_number= product_number
    dict.notes= notes
    dict.update_user = uid(request)
    dict.update_time = update_time

    # 更新数据
    dict.save()
    # 返回结果
    return R.ok(msg="更新成功")


# 删除字典
def DictDelete(dict_id):
    # 记录ID为空判断
    if not dict_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = dict_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            # 根据ID查询记录
            dict = Dict.objects.only('id').filter(id=int(id), is_delete=False).first()
            # 查询结果判空
            if not dict:
                return R.failed("字典不存在")
            # 设置删除标识
            dict.is_delete = True
            # 更新记录
            dict.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


def SupplierBatchAdd(request):
    # 接收请求参数
    json_data = request.body.decode()
    # 参数为空判断
    if not json_data:
        return R.failed("参数不能为空")
        # 数据类型转换
    dict_data = json.loads(json_data)

    work_order = dict_data.get('work_order')
    customer = dict_data.get('customer')
    product_name = dict_data.get('product_name')
    product_type = dict_data.get('product_type')
    supplier = dict_data.get('supplier')
    parts = dict_data.get('parts')
    product_number = dict_data.get('product_number')
    notes = dict_data.get('notes')
    PCB_code = dict_data.get('PCB_code')
    part_code = dict_data.get('part_code')

    Dict.objects.create(
        work_order=work_order,
        customer = customer,
        product_name = product_name,
        product_type = product_type,
        supplier = supplier,
        parts = parts,
        product_number = product_number,
        notes =notes,
        PCB_code = PCB_code,
        part_code = part_code,
    )

    # 返回结果
    return R.ok(msg="添加数据成功！")