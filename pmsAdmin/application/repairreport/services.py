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
from application.user.services import UserDetail#绑定维修员真实id
from django.core.paginator import Paginator
from django.db.models import Q#查询用的
from application.repairreport import forms
from application.repairreport.models import Dict
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
    repair_user = request.GET.get('repair_user')
    if repair_user:
       query = query.filter(repair_user__contains=repair_user)

    # 按关键字查询
    # keyword = request.GET.get('keyword')
    # if keyword:
    #     query = query.filter(
    #         Q(commit_user__icontains=keyword) |  # commit_user字段包含关键字
    #         Q(item_number__icontains=keyword) |  # item_number字段包含关键字
    #         Q(work_order_id__icontains=keyword)  # work_order_id字段包含关键字
    #    )
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
        for item in dict_list:

            data = {
                'id': item.id,
                'repair_user': item.repair_user,
                'name': item.name,
                'work_order': item.work_order,
                'bad_number': item.bad_number,
                'repair_number': item.repair_number,
                'bad_phenomenon': item.bad_phenomenon,
                'analysis': item.analysis,
                'solution': item.solution,
                'notes': item.notes,
                'create_user':item.create_user,
                'repair_time': str(item.repair_time.strftime('%Y-%m-%d %H:%M:%S')) if item.repair_time else None,
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

    data = {
        'id': dict.id,
        'repair_user': dict.repair_user,
        'name': dict.name,
        'work_order': dict.work_order,
        'bad_number': dict.bad_number,
        'repair_number': dict.repair_number,
        'bad_phenomenon': dict.bad_phenomenon,
        'analysis': dict.analysis,
        'solution': dict.solution,
        'notes': dict.notes,
        'repair_time': str(dict.repair_time.strftime('%Y-%m-%d %H:%M:%S')) if dict.repair_time else None,

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
        #goods = Dict.objects.filter(name=dict_data.get('order_id')).first()
        #if goods:
            #return R.failed("工单号已存在")

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
        name = form.cleaned_data.get('name')
        work_order = form.cleaned_data.get('work_order')
        bad_number = form.cleaned_data.get('bad_number')
        repair_number = form.cleaned_data.get('repair_number')
        bad_phenomenon = form.cleaned_data.get('bad_phenomenon')
        analysis = form.cleaned_data.get('analysis')
        solution = form.cleaned_data.get('solution')
        notes = form.cleaned_data.get('notes')
        repair_time = form.cleaned_data.get('repair_time')
        # 创建数据
        Dict.objects.create(
            #name=name,
            #code=code,
            #sort=sort,
            #note=note,
            repair_user=UserDetail(uid(request)).get("realname"),
            name=name,
            work_order=work_order,
            bad_number=bad_number,
            repair_number=repair_number,
            bad_phenomenon=bad_phenomenon,
            analysis=analysis,
            solution=solution,
            notes=notes,
            repair_time=repair_time,
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
        name = form.cleaned_data.get('name')
        work_order = form.cleaned_data.get('work_order')
        bad_number = form.cleaned_data.get('bad_number')
        repair_number = form.cleaned_data.get('repair_number')
        bad_phenomenon = form.cleaned_data.get('bad_phenomenon')
        analysis = form.cleaned_data.get('analysis')
        solution = form.cleaned_data.get('solution')
        notes = form.cleaned_data.get('notes')
        repair_time = form.cleaned_data.get('repair_time')
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
    dict.name = name
    dict.work_order=work_order
    dict.bad_number = bad_number
    dict.repair_number = repair_number
    dict.bad_phenomenon = bad_phenomenon
    dict.analysis = analysis
    dict.solution = solution
    dict.notes = notes
    dict.repair_time = repair_time
    dict.update_user = uid(request)

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
#获取产品名称
def Dictnamelist(request):
    sql1 = "select id,name, count( name) as namenum from django_repairreport where is_delete=False group by name  order by  namenum desc limit 10"
    namelist = Dict.objects.raw(sql1)
    name_list=[]
    if namelist:
        for item in namelist:
            data = {
                'value': item.name,
            }
            name_list.append(data)
    return name_list
#获取不良现象
def Dictbad_phenomenonlist(request):
    name = request.GET.get('name')
    sql2 = "select id, bad_phenomenon, count( bad_phenomenon) as badnum from django_repairreport where name = %s and is_delete=False group by bad_phenomenon order by  badnum desc limit 10;"
    bad_phenomenonlist = Dict.objects.raw(sql2,[name])
    bad_phenomenon_list=[]
    if bad_phenomenonlist:
        for item in bad_phenomenonlist:
            data = {
                'value': item.bad_phenomenon,
            }
            bad_phenomenon_list.append(data)
    return bad_phenomenon_list
#获取原因分析
def Dictanalysislist(request):
    name = request.GET.get('name')
    sql3 = "select id,analysis, count( analysis) as analysisnum from django_repairreport where name = %s and is_delete=False group by analysis order by analysisnum desc limit 10;"
    analysislist = Dict.objects.raw(sql3,[name])
    analysis_list=[]
    if analysislist:
        for item in analysislist:
            data = {
                'value': item.analysis,
            }
            analysis_list.append(data)
    return analysis_list
#获取解决方法
def Dictsolutionlist(request):
    name = request.GET.get('name')
    sql4 = "select id,solution, count( solution) as solutionnum from django_repairreport where name = %s and is_delete=False group by solution order by solutionnum desc limit 10;"
    solutionlist = Dict.objects.raw(sql4,[name])
    solution_list=[]
    if solutionlist:
        for item in solutionlist:
            data = {
                'value': item.solution,
            }
            solution_list.append(data)
    return solution_list



#图表数据传输
def RepairreportListOfTotal(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Dict.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        #sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,name, bad_number, repair_number, analysis,sum(bad_number) AS bad_total, sum(repair_number) AS repair_total FROM django_repairreport WHERE is_delete = 0  AND create_time >= %s AND create_time <= %s GROUP BY id"
        query = Dict.objects.raw(sql,[startTime, endTime])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        sql = "SELECT id,name, bad_number, repair_number, analysis, sum(bad_number) AS bad_total, sum(repair_number) AS repair_total FROM django_repairreport WHERE is_delete = 0 GROUP BY  id"
        query = Dict.objects.raw(sql)
        paginator = Paginator(query, limit)

    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0:
        for item in producerecord_list:
            item.rate=str(item.repair_total)+str("/")+str(item.bad_total)
            data = {
                'id': item.id,
                'name': item.name,
                'bad_phenomenon': item.bad_phenomenon,
                'analysis':item.analysis,
                'repair_total':item.repair_total,
                'bad_total':item.bad_total,
                'rate':item.rate,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

#柱状图数据传输
def RepairreportListOfTotal1(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Dict.objects.filter(is_delete=False)
    startTime = request.GET.get('startTime')
    endTime = request.GET.get('endTime')
    if startTime and endTime:
        startTime = startTime.replace("+", " ")
        endTime = endTime.replace("+", " ")
        #sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,name, sum(bad_number) AS bad_total, sum(repair_number) AS repair_total FROM django_repairreport WHERE is_delete = 0  AND create_time >= %s AND create_time <= %s GROUP BY name "
        query = Dict.objects.raw(sql,[startTime, endTime])
        # 设置分页
        paginator = Paginator(query, limit)
    else:
        sql = "SELECT id,name, sum(bad_number) AS bad_total, sum(repair_number) AS repair_total FROM django_repairreport WHERE is_delete = 0 GROUP BY name"
        query = Dict.objects.raw(sql)
        paginator = Paginator(query, limit)

    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0:
        for item in producerecord_list:
            item.rate=str(item.repair_total)+str("/")+str(item.bad_total)
            data = {
                'id': item.id,
                'name': item.name,
                'repair_total':item.repair_total,
                'bad_total':item.bad_total,
                'rate':item.rate,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)

#问题清单数据传输
def QuestionList(request):
    # 页码
    page = int(request.GET.get("page", 1))
    # 每页数
    limit = int(request.GET.get("limit", PAGE_LIMIT))
    # 实例化查询对象
    query = Dict.objects.filter(is_delete=False)
    name = request.GET.get('name')
    work_order = request.GET.get('work_order')
    if name :
        # sql = 'SELECT item_number,sum(examine_an_amount) AS total,sum(examine_a_bad_amount) AS badtotal FROM django_inspectreport WHERE is_delete = 0 AND start_time >= ' + str(startTime) + ' AND end_time <= ' + str(endTime)+ " GROUP BY item_number" + " limit " + str(limit)
        sql = "SELECT id,name, work_order, bad_phenomenon, count( bad_phenomenon) as num  FROM django_repairreport WHERE is_delete = 0 GROUP BY %s ,bad_phenomenon ORDER BY %s,num Desc"
        query = Dict.objects.raw(sql, [name])
        # 设置分页
        paginator = Paginator(query, limit)
    elif work_order:
        sql = "SELECT id,name, work_order, bad_phenomenon, count( bad_phenomenon) as num  FROM django_repairreport WHERE is_delete = 0 GROUP BY %s ,bad_phenomenon ORDER BY %s,num Desc"
        query = Dict.objects.raw(sql,[work_order])
        paginator = Paginator(query, limit)

    # 记录总数
    count = paginator.count
    # 分页查询
    producerecord_list = paginator.page(page)
    # 实例化结果
    result = []
    # 遍历数据源
    if len(producerecord_list) > 0:
        for item in producerecord_list:
            data = {
                'id': item.id,
                'name': item.name,
                'work_order': item.work_order,
                'bad_phenomenon':item.bad_phenomenon,
                'num':item.num,
            }
            result.append(data)
    # 返回结果
    return R.ok(data=result, count=count)


