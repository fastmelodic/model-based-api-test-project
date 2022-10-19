def get_missing_fields(unsent_fields: set, service_resonse: dict) -> set:
    error_data = set(tuple(i) for i in [i['loc'][1:] for i in service_resonse if i['msg'] == 'field required'])

    return unsent_fields.difference(error_data)
