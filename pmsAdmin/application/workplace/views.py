from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from . import services
from middleware.login_middleware import check_login
from utils import R

#查询生产总数量
@method_decorator(check_login, name='get')
class ShipmentAllView(View):
    def get(self, request):
        data = services.ShipmentAll()
        return R.ok(data=data)

#获取总成品合格率
@method_decorator(check_login, name='get')
class AllPassView(View):
    def get(self, request):
        data = services.AllPass()
        return R.ok(data=data)


#获取总的工具使用时长
@method_decorator(check_login, name='get')
class AllUseToolTimeView(View):
    def get(self, request):
        data = services.AllUseToolTime()
        return R.ok(data=data)

#获取所有生产模块的数据
@method_decorator(check_login, name='get')
class AllModelsDataView(View):
    def get(self, request):
        data = services.AllModelsData(request)
        return  R.ok(data=data)

#获取所有生产成品的数据
@method_decorator(check_login, name='get')
class AllFinishedDataView(View):
    def get(self, request):
        data = services.AllFinishedData(request)
        return  R.ok(data=data)

#获取工具使用时长
@method_decorator(check_login, name='get')
class GetToolUseTimeView(View):
    def get(self, request):
        data = services.GetToolUseTime(request)
        return  R.ok(data=data)