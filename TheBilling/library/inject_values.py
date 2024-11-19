def inject_values(obj: object, fields: list[str]):
    # добавляет в объект перед передачей в шаблон свойство addons,
    # содержащее список значений свойств объекта из листа fields
    values = list()
    for field in fields:
        v = getattr(obj, field)
        if hasattr(v, 'all'):
            v = [str(x) for x in v.all()]
        values.append(v)
    obj.addons = values
    return obj