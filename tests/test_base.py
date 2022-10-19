from api.client import order_base_client
from resources.prepare_data import prepare_data
from serializers.orders import Order


def test_base():

    order = prepare_data('create_order')
    create_order = order_base_client.create_order(order)
    order_id = create_order.json()['id']

    get_order = order_base_client.get_order(order_id)

    assert Order(**order).dict() == Order(**get_order.json()).dict()
    assert get_order.status_code == 204, f'{get_order.json()}'
    assert get_order.content == b''
