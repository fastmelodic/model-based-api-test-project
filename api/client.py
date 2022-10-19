import requests


class OrderBaseClient:
    url = "https://some.url"

    def create_order(self, order):
        # Создание заказа
        return requests.post(self.url + '/orders', json=order)

    def get(self, order_id):
        # Получение заказа
        return requests.get(self.url + f'/orders/{order_id}')


order_base_client = OrderBaseClient()
