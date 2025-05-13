from .BaseService import BaseService


class UserService(BaseService):
    # ...existing code...

    def get_city_list(self):
        api_method = "u-city-list"
        return self.call_api(api_method, True)
