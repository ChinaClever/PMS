from application.bind.product.models import Product


# 根据调试数据ID查询测试步骤列表
def getModuleList(productId):
    sql = 'SELECT * FROM django_bind_module WHERE product_id=%s'
    list = Product.objects.raw(sql, [productId])
    # 实例化测试步骤列表
    module_list = []
    if list:
        for v in list:
            item = {
                'key': v.key,
            }
            # 加入数组
            module_list.append(item)
    # 返回结果
    return module_list
