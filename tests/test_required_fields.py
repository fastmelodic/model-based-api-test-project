import pytest

from api.client import order_base_client
from resources.prepare_data import prepare_data
from helpers.general import get_missing_fields
from helpers.models import delete_fields, get_required_fields_paths, parametrize_list_of_objects
from serializers.orders import Order


fields_to_test = parametrize_list_of_objects(Order, required=True)


@pytest.mark.parametrize('model, path', fields_to_test)
def test_required_fields(model, path):

    order = prepare_data('create_order')

    fields_to_delete = get_required_fields_paths(model, path)
    delete_fields('required', order, model, path)

    create_order = order_base_client.create_order(order)

    assert create_order.status_code == 422, f'{create_order.text}'
    missing_fields = get_missing_fields(fields_to_delete, create_order.json()['detail'])
    assert len(missing_fields) == 0, missing_fields
