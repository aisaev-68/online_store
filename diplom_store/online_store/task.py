data = [{'filter[specifications][0][key]': 'Объем встроенной памяти'}, {'filter[specifications][0][value]': '8 ГБ'}, {'filter[specifications][1][key]': 'Объем встроенной памяти'}, {'filter[specifications][1][value]': '16 ГБ'}, {'filter[specifications][2][key]': 'Объем встроенной памяти'}, {'filter[specifications][2][value]': '64 ГБ'}, {'filter[specifications][3][key]': 'Разрешение экрана'}, {'filter[specifications][3][value]': '2732x2048'}, {'filter[specifications][4][key]': 'Разрешение экрана'}, {'filter[specifications][4][value]': '2960x1848'}]

result = {}
for item in data:
    key = next(iter(item))  # Получаем ключ словаря
    value = item[key]  # Получаем значение словаря
    # Извлекаем информацию из ключа
    if 'key' in key:
        property_key = value
        if property_key not in result:
            result[property_key] = []
    else:
        result[property_key].append(value)

print(result)