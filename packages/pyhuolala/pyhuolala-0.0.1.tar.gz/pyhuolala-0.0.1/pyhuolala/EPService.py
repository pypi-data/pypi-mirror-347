from .BaseService import BaseService


class EPService(BaseService):
    # 获取城市列表
    def get_city_list(self):
        api_method = "e-city-list"
        return self.call_api(api_method)

    # 获取订单详情
    def order_detail(self, order_display_id):
        api_method = "e-order-detail"
        api_data = {"order_display_id": order_display_id}
        return self.call_api(api_method, api_data)
