from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from . import services
from middleware.login_middleware import check_login
from utils import R

#获取维修的数据
@method_decorator(check_login, name='get')
class RepairDataView(View):
    def get(self, request):
        data = services.RepairData(request)
        return  data

@method_decorator(check_login, name='get')
class ResultDataView(View):
    def get(self, request):
        data = services.ResultData(request)
        return  data
