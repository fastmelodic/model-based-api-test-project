from pydantic.main import ModelMetaclass as PydanticModel

from serializers.orders import *


def delete_fields(flag: str, data: dict, model: PydanticModel, paths: list | tuple) -> None:
    if isinstance(paths, tuple):
        paths = [paths]

    fields_to_delete = []
    if flag == 'required':
        fields_to_delete = model.schema()['required']
    elif flag == 'optional':
        fields_to_delete = _get_optional_fields(model)

    for item in paths:
        obj = _get_value_by_path(data, item)
        for field in fields_to_delete:
            obj.pop(field)


def get_required_fields_paths(model: PydanticModel, path: tuple | list) -> set:
    paths = set()
    required_fields = _get_required_fields(model)

    if isinstance(path, list):
        for i in range(len(path)):
            for field in required_fields:
                paths.add(path[i]+(field,))
    elif isinstance(path, tuple):
        for field in required_fields:
            paths.add(path+(field,))

    return paths


def parametrize_list_of_objects(model: PydanticModel, required: bool = False) -> list:
    objects = []
    if required:
        try:
            _get_required_fields(model)
            objects = [(model, ())]
        except KeyError:
            pass
    _build_list_for_parametrize(model, objects, (), required)
    return objects


def _get_value_by_path(data: dict, path: tuple) -> dict:
    current_val = data
    for key in path:
        current_val = current_val[key]

    return current_val


def _get_required_fields(model: PydanticModel) -> list:
    if '$ref' in model.schema():
        required_fields = model.schema()['definitions'][f'{model.__name__}']['required']
    else:
        required_fields = model.schema()['required']

    return required_fields


def _get_optional_fields(model: PydanticModel) -> list:
    if '$ref' in model.schema():
        all_fields = set(model.schema()['definitions'][f'{model.__name__}']['properties'].keys())
    else:
        all_fields = set(model.schema()['properties'].keys())

    try:
        required_fields = set(_get_required_fields(model))
    except KeyError:
        required_fields = set()

    return list(all_fields.difference(required_fields))


def _build_list_for_parametrize(model: PydanticModel, built_list_of_fields: list, path: tuple, required: bool) -> None:
    fields_properties = model.schema()['properties']
    for i in fields_properties:
        is_list = False
        obj = {}
        if 'type' in fields_properties[i]:
            if fields_properties[i]['type'] == 'array':
                obj = fields_properties[i]['items']
                is_list = True
        else:
            obj = fields_properties[i]

        if '$ref' in obj:
            child_model = globals()[obj['$ref'][14:]]
            if required:
                try:
                    _get_required_fields(child_model)
                except KeyError:
                    continue
            if is_list:
                local_path = path + (i, 0)
            else:
                local_path = path + (i,)
            built_list_of_fields.append((child_model, local_path))
            _build_list_for_parametrize(child_model, built_list_of_fields, local_path, required)
