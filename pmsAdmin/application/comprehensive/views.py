from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from . import services
from middleware.login_middleware import check_login
from utils import R

#获取所有的数据
@method_decorator(check_login, name='get')
class DetailAllView(View):
    def get(self, request):
        data = services.DetailAll(request)
        return  data

@method_decorator(check_login, name='get')
class getShipmentDataView(View):
    def get(self, request):
        data = services.getShipmentData(request)
        return  data
