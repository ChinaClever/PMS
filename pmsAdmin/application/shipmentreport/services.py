
import os
import uuid
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db import transaction
from django.db.models import Q
from application.shipmentreport.models import Shipment
from application.shipmentreport.models import Product
from constant.constants import PAGE_LIMIT
from utils import R

# 查询分页数据
from utils.utils import uid


def ShipmentReportList(request):
    # 页码
    page = int(request.GET.get('page', 1))
    # 每页数
    limit = int(request.GET.get('limit', PAGE_LIMIT))
    # 筛选成品 模块
    product_module = request.GET.get('product_module')
    query = Shipment.objects.filter(is_delete=False)
    # 查询数据
    if product_module:
        query = Shipment.objects.filter(is_delete=False, product_module = product_module)
    # else:
    #     query = Shipment.objects.filter(is_delete=False, product_module=1)
    # 模糊筛选
    keyword  = request.GET.get('keyword')
    if keyword :
        query = query.filter(
            Q(client_name__icontains=keyword) |
            Q(product_name__icontains=keyword) |
            Q(work_order__icontains=keyword)
        )
    # 筛选年份
    year = request.GET.get('year')
    if year:
        query = query.filter(delivery_date__year=int(year))

    # 筛选月份
    month = request.GET.get('month')
    if month:
        query = query.filter(delivery_date__month=int(month))

    # 筛选年月范围
    selectStartDate = request.GET.get('selectStartDate')
    selectEndDate = request.GET.get('selectEndDate')
    if selectStartDate and selectEndDate:
        start_date = datetime.strptime(selectStartDate, "%Y-%m-%d")
        end_date = datetime.strptime(selectEndDate, "%Y-%m-%d")
        query = query.filter(order_date__gte=start_date, order_date__lte=end_date)

    # 排序
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort and order:
        query = query.order_by(f'-{sort}' if order == 'desc' else sort)
    else:
        query = query.order_by("-id")
    # 分页设置
    paginator = Paginator(query, limit)
    # 记录总数
    count = paginator.count
    # 分页查询
    try:
        shipmentreport_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        shipmentreport_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        shipmentreport_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return R.failed('找不到页面的内容')
    # 遍历数据源
    result = []
    # 总数量
    items_total = 0
    if len(shipmentreport_list) > 0:
        for item in shipmentreport_list:
            data = {
                'id': item.id,
                'work_order': item.work_order,
                'client_name': item.client_name,
                'product_code': item.product_code,
                'product_name': item.product_name,
                'shape': item.shape,
                'order_date': str(item.order_date.strftime('%Y-%m-%d')),
                'delivery_date': str(item.delivery_date.strftime('%Y-%m-%d')),
                'update_delivery_date': str(item.update_delivery_date.strftime('%Y-%m-%d')) if item.update_delivery_date else None,
                'finish_date': str(item.finish_date.strftime('%Y-%m-%d')) if item.finish_date else None,
                'product_count': item.product_count,
                'SO_RQ_id': item.SO_RQ_id if item.SO_RQ_id else None,
                'remark': item.remark if item.remark else None,
                'product_module': item.product_module,
                'attachment': item.attachment if item.attachment else None,
                'create_time': str(item.create_time.strftime('%Y-%m-%d')) if item.create_time else None,
                'update_time': str(item.update_time.strftime('%Y-%m-%d')) if item.create_time else None,
            }
            items_total += item.product_count
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count, items_total=items_total)


def ShipmentReportDetail(shipment_id):
    # 根据ID查询
    shipment = Shipment.objects.filter(is_delete=False, id=shipment_id).first()
    # 查询结果判空
    if not shipment:
        return None
    # 声明结构体
    data = {
        'id': shipment.id,
        'work_order': shipment.work_order,
        'client_name': shipment.client_name,
        'product_code': shipment.product_code,
        'product_name': shipment.product_name,
        'shape': shipment.shape,
        'order_date': str(shipment.order_date.strftime('%Y-%m-%d')),
        'delivery_date': str(shipment.delivery_date.strftime('%Y-%m-%d')),
        'update_delivery_date': str(shipment.update_delivery_date.strftime('%Y-%m-%d')) if shipment.update_delivery_date else None,
        'finish_date': str(shipment.finish_date.strftime('%Y-%m-%d')) if shipment.finish_date else None,
        'product_count': shipment.product_count,
        'SO_RQ_id': shipment.SO_RQ_id,
        'remark': shipment.remark if shipment.remark else None,
        'product_module': shipment.product_module,
        'attachment': shipment.attachment if shipment.attachment else None,

    }
    # 返回结果
    return data

@transaction.atomic
def ShipmentReportAdd(request):
    work_order = request.POST.get('work_order')
    client_name = request.POST.get('client_name')
    product_code = request.POST.get('product_code')
    product_name = request.POST.get('product_name')
    shape = request.POST.get('shape')
    order_date = request.POST.get('order_date')
    delivery_date = request.POST.get('delivery_date')
    finish_date = request.POST.get('finish_date')
    product_count = request.POST.get('product_count')
    SO_RQ_id = request.POST.get('SO_RQ_id')
    remark = request.POST.get('remark')
    product_module = request.POST.get('product_module')
    # 根据work_order查询 不能有相同工单号
    isWorkOrderExist = Shipment.objects.only('id').filter(work_order=work_order, is_delete=False).first()
    if isWorkOrderExist:
        return R.failed("工单号已存在")

    FileSavePath = "public/uploads/shipmentFiles"
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

    Shipment.objects.create(
        work_order=work_order,
        client_name=client_name,
        product_code=product_code,
        product_name=product_name,
        shape=shape,
        order_date=order_date,
        delivery_date=delivery_date,
        finish_date=finish_date if finish_date else None,
        product_count=product_count,
        SO_RQ_id=SO_RQ_id,
        product_module=product_module,
        remark=remark if remark else None,
        attachment = attachmentListToString if files else None,
        create_user=uid(request)
        )

    product = Product.objects.filter(product_code=product_code, is_delete=False).first()
    # 查询结果判断
    if not product:
        Product.objects.create(
            product_code=product_code,
            product_name=product_name,
            shape=shape,
            product_module=product_module,
        )

    return R.ok(msg="创建成功")


@transaction.atomic
def ShipmentReportUpdate(request):
    # ID
    shipment_id = request.POST.get('id')
    # ID判空
    if not shipment_id or int(shipment_id) <= 0:
        return R.failed("ID不能为空")
    # 根据ID查询
    shipment = Shipment.objects.only('id').filter(id=shipment_id, is_delete=False).first()
    # 查询结果判断
    if not shipment:
        return R.failed("数据不存在,请重试！")
    # 根据work_order查询 不能有相同工单号
    work_order = request.POST.get('work_order')
    isWorkOrderExist = Shipment.objects.only('id').filter(work_order=work_order, is_delete=False).exclude(id=shipment_id).first()
    if isWorkOrderExist:
        return R.failed("工单号已存在")

    FileSavePath = "public/uploads/shipmentFiles"
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

    client_name = request.POST.get('client_name')
    product_code = request.POST.get('product_code')
    product_name = request.POST.get('product_name')
    shape = request.POST.get('shape')
    order_date = request.POST.get('order_date')
    delivery_date = request.POST.get('delivery_date')
    update_delivery_date = request.POST.get('update_delivery_date')
    finish_date = request.POST.get('finish_date')
    product_count = request.POST.get('product_count')
    SO_RQ_id = request.POST.get('SO_RQ_id')
    remark = request.POST.get('remark')
    product_module = request.POST.get('product_module')

    # 日期格式转化
    if update_delivery_date == "null":
        update_delivery_date = ""
    if finish_date == "null":
        finish_date = ""

    # 删除文件
    deleteFileList = request.POST.get('deleteFileList')
    # 使用逗号分割字符串，得到文件路径列表
    file_paths = shipment.attachment.split(',') if shipment.attachment else []

    if deleteFileList:
        # 提取文件名列表
        file_names = [path.split('_', 1)[-1] for path in file_paths]
        print(file_names)
        for index,file_name in enumerate(file_names):
            # 存在deleteFileList列表中 表示要删除
            if file_name in deleteFileList:
                delete_file_path = 'public/'+file_paths[index]
                try:
                    os.remove(delete_file_path)
                    print(delete_file_path+"文件删除成功")
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
        attachmentListToString = shipment.attachment

    # 保存原先的product_code 方便更新product表
    origin_product_code = shipment.product_code
    # 对象赋值
    shipment.work_order = work_order
    shipment.client_name = client_name
    shipment.product_code = product_code
    shipment.product_name = product_name
    shipment.shape = shape
    shipment.order_date = order_date
    shipment.delivery_date = delivery_date
    shipment.finish_date = finish_date if finish_date else None
    shipment.update_delivery_date = update_delivery_date if update_delivery_date else None
    shipment.product_count = product_count
    shipment.SO_RQ_id = SO_RQ_id
    shipment.remark = remark
    shipment.product_module = product_module
    shipment.attachment = attachmentListToString
    shipment.update_user = uid(request)
    shipment.update_time = datetime.now()
    shipment.save()

    isProductExist = Product.objects.filter(is_delete=False, product_code=product_code).first()
    # 修改了一个新的成品编码(数据库里没有) 这时添加一条数据
    if not isProductExist:
        if origin_product_code != product_code:
            Product.objects.create(
                product_code=product_code,
                product_name=product_name,
                shape=shape,
                product_module=product_module,
            )
        else:
            # 没修改成品编码 则更新product表 用原先的product_code查
            product = Product.objects.filter(is_delete=False, product_code=origin_product_code).first()
            if not product:
                return R.failed("产品数据不存在")
            product.product_name = product_name
            product.shape = shape
            product.product_module = product_module
            product.update_user = uid(request)
            product.update_time = datetime.now()
            product.save()
    # 返回结果
    return R.ok(msg="更新成功")


def ShipmentReportDelete(shipment_id):
    if not shipment_id:
        return R.failed("记录ID不存在")
    # 分裂字符串
    list = shipment_id.split(',')
    # 计数器
    count = 0
    # 遍历数据源
    if len(list) > 0:
        for id in list:
            shipment = Shipment.objects.only('id').filter(id=int(id), is_delete=False).first()
            if not shipment:
                return R.failed("数据不存在")
            # 设置删除标识
            shipment.is_delete = True
            # 更新记录
            shipment.save()
            # 计数器+1
            count += 1
    # 返回结果
    return R.ok(msg="本次共删除{0}条数据".format(count))


# 根据产品编码查产品名称 规格
def SelectProdcutDetailByProductCode(product_code):
    product = Product.objects.filter(is_delete=False, product_code=product_code).first()
    if not product:
        return None

    data = {
        'id': product.id,
        'product_code': product.product_code,
        'product_name': product.product_name,
        'shape': product.shape,
        'product_module': product.product_module,
    }
    return data

# 获取所有产品名称（不重复）
def ProductNameList(request):
    productNameList = Product.objects.filter(is_delete=False)
    result = []
    existing_names = set()  # 存储已存在的product_name值
    if len(productNameList) > 0:
        for item in productNameList:
            product_name = item.product_name
            if product_name not in existing_names:
                data = {
                    'value': product_name,
                }
                result.append(data)
                existing_names.add(product_name)
    # 返回结果
    return result

# 获取所有工单号 倒序返回
def WorkOrderList(request):
    workOrderList = Shipment.objects.filter(is_delete=False).order_by('-id').values_list('work_order', flat=True)
    result = []
    if len(workOrderList) > 0:
        for item in workOrderList:
            data = {
                'value': item
            }
            result.append(data)

    return result

# 根据工单号查详情
def SelectShipmentDetailByWorkOrder(work_order):
    shipment = Shipment.objects.filter(is_delete=False, work_order=work_order).first()
    # 查询结果判空
    if not shipment:
        return None
    # 声明结构体
    data = {
        'id': shipment.id,
        'work_order': shipment.work_order,
        'client_name': shipment.client_name,
        'product_code': shipment.product_code,
        'product_name': shipment.product_name,
        'shape': shipment.shape,
        'order_date': str(shipment.order_date.strftime('%Y-%m-%d')),
        'delivery_date': str(shipment.delivery_date.strftime('%Y-%m-%d')),
        'update_delivery_date': str(shipment.update_delivery_date.strftime('%Y-%m-%d')) if shipment.update_delivery_date else None,
        'finish_date': str(shipment.finish_date.strftime('%Y-%m-%d')) if shipment.finish_date else None,
        'product_count': shipment.product_count,
        'SO_RQ_id': shipment.SO_RQ_id,
        'remark': shipment.remark if shipment.remark else None,
        'product_module': shipment.product_module,
        'attachment': shipment.attachment if shipment.attachment else None,
    }
    # 返回结果
    return data


