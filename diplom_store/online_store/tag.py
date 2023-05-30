import requests
import json


def get_data():
    cookies = {
        '_ym_uid': '1648377972324637575',
        '_ym_d': '1669908228',
        'cfidsgib-w-mvideo': 'JtN2NBktjPo03HY3WcMc+qaIwJ7KLB7bQSLZTd43fPqGLJTCmu63URL/cZeJ5LGImGgpJh1iPSsXSd+jbBwcfqR48MKjqPFI35ZwcOQG70WVP84XsRJriuLrnDhrbgXtfhasy+O7QB8mqAw6+DqkKNNcuOuLTc1fkYwp',
        '__lhash_': '8b885b00133fea6ad5b62fa2e0302828',
        'MVID_ACTOR_API_AVAILABILITY': 'true',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': 'CityCZ_974',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLC': 'true',
        'MVID_GLP': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_IMG_RESIZE': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '5200000100000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '118',
        'MVID_REGION_SHOP': 'S902',
        'MVID_SERVICES': '111',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_WEBP_ENABLED': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        '_gid': 'GA1.2.1039158232.1674067771',
        '_sp_ses.d61c': '*',
        '_ym_isad': '1',
        '__SourceTracker': 'yandex.ru__organic',
        'admitad_deduplication_cookie': 'yandex.ru__organic',
        'SMSError': '',
        'authError': '',
        'tmr_lvid': '5fdb1415d9e9d1bd7a57c2bf234a246a',
        'tmr_lvidTS': '1651343037354',
        'flocktory-uuid': '4384ce1b-18eb-4e90-a94b-f032920253e0-5',
        'advcake_track_id': '62775072-2db9-bcca-8f62-8a47e4cbd38f',
        'advcake_session_id': '7f364c6f-a074-09d8-1a83-1947ecd6e197',
        'afUserId': '4a1203c3-e58f-4735-8457-79c75f6e0dd2-p',
        'AF_SYNC': '1674067776465',
        '_ga': 'GA1.2.214670125.1674067771',
        'tmr_detect': '1%7C1674068108120',
        '_dc_gtm_UA-1873769-1': '1',
        '_dc_gtm_UA-1873769-37': '1',
        '_sp_id.d61c': '5e78d049-b5e7-427c-9a36-b2837ffb0680.1669908228.4.1674068268.1670946441.f09adcfa-7867-4951-acc0-8d26f9606cd8.5c4a4eb2-77d2-41ac-a9e0-3ea8c832236c.891bc6b3-7a08-46da-83a8-b02e22c66c64.1674067771383.43',
        '_ga_CFMZTSS5FM': 'GS1.1.1674067771.1.1.1674068273.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1674067771.1.1.1674068273.54.0.0',
        'MVID_ENVCLOUD': 'prod2',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=d1f99623dbb844459e37e6f0305e9d31,sentry-sample_rate=0.5',
        # 'cookie': '_ym_uid=1648377972324637575; _ym_d=1669908228; cfidsgib-w-mvideo=JtN2NBktjPo03HY3WcMc+qaIwJ7KLB7bQSLZTd43fPqGLJTCmu63URL/cZeJ5LGImGgpJh1iPSsXSd+jbBwcfqR48MKjqPFI35ZwcOQG70WVP84XsRJriuLrnDhrbgXtfhasy+O7QB8mqAw6+DqkKNNcuOuLTc1fkYwp; __lhash_=8b885b00133fea6ad5b62fa2e0302828; MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_974; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=5200000100000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=118; MVID_REGION_SHOP=S902; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_WEBP_ENABLED=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.1039158232.1674067771; _sp_ses.d61c=*; _ym_isad=1; __SourceTracker=yandex.ru__organic; admitad_deduplication_cookie=yandex.ru__organic; SMSError=; authError=; tmr_lvid=5fdb1415d9e9d1bd7a57c2bf234a246a; tmr_lvidTS=1651343037354; flocktory-uuid=4384ce1b-18eb-4e90-a94b-f032920253e0-5; advcake_track_id=62775072-2db9-bcca-8f62-8a47e4cbd38f; advcake_session_id=7f364c6f-a074-09d8-1a83-1947ecd6e197; afUserId=4a1203c3-e58f-4735-8457-79c75f6e0dd2-p; AF_SYNC=1674067776465; _ga=GA1.2.214670125.1674067771; tmr_detect=1%7C1674068108120; _dc_gtm_UA-1873769-1=1; _dc_gtm_UA-1873769-37=1; _sp_id.d61c=5e78d049-b5e7-427c-9a36-b2837ffb0680.1669908228.4.1674068268.1670946441.f09adcfa-7867-4951-acc0-8d26f9606cd8.5c4a4eb2-77d2-41ac-a9e0-3ea8c832236c.891bc6b3-7a08-46da-83a8-b02e22c66c64.1674067771383.43; _ga_CFMZTSS5FM=GS1.1.1674067771.1.1.1674068273.0.0.0; _ga_BNX5WPP3YK=GS1.1.1674067771.1.1.1674068273.54.0.0; MVID_ENVCLOUD=prod2',
        'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/planshety-195?reff=menu_main',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'd1f99623dbb844459e37e6f0305e9d31-8d7e189e7c29dde5-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-set-application-id': 'a10a02fa-e59c-4a9c-a077-c22083fc4170',
    }

    params = {
        'categoryId': '195',
        'offset': '0',
        'limit': '24',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'doTranslit': 'true',
    }

    # Получаем список планшетов
    response = requests.get('https://www.mvideo.ru/bff/products/listing',
                            params=params, cookies=cookies, headers=headers).json()
    # print(response)
    print(response)
    # Вытаскиваем id продуктов
    products_ids = response.get('body').get('products')

    # Полученные id записываем в файл
    with open('1_products_ids.json', 'w') as file:
        json.dump(products_ids, file, indent=4, ensure_ascii=False)

    # print(products_ids)
    json_data = {
        'productIds': products_ids,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
    }

    response = requests.post('https://www.mvideo.ru/bff/product-details/list',
                             cookies=cookies, headers=headers, json=json_data).json()

    with open("2_items.json", "w") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    products_ids_str = ','.join(products_ids)

    params = {
        'productIds': products_ids_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/prices',
                            params=params, cookies=cookies, headers=headers).json()

    with open("3_prices.json", "w") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    items_prices = {}
    material_prices = response.get('body').get('materialPrices')

    for item in material_prices:
        item_id = item.get('price').get('productId')
        item_base_price = item.get('price').get('basePrice')
        item_sale_price = item.get('price').get('salePrice')
        item_bonus = item.get('bonusRubles').get('total')

        items_prices[item_id] = {
            'item_base_price': item_base_price,
            'item_sale_price': item_sale_price,
            'item_bonus': item_bonus
        }

    with open("4_items_prices.json", "w") as file:
        json.dump(items_prices, file, indent=4, ensure_ascii=False)


def get_result():
    with open('2_items.json') as file:
        products_data = json.load(file)

    with open('4_items_prices.json') as file:
        products_prices = json.load(file)

    products_data = products_data.get('body').get('products')

    for item in products_data:
        product_id = item.get('productId')

        if product_id in products_prices:
            prices = products_prices[product_id]

            item['item_base_price'] = prices.get('item_base_price')
            item['item_sale_price'] = prices.get('item_sale_price')
            item['item_bonus'] = prices.get('item_bonus')

    with open("5_results.json", "w") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    get_result()


if __name__ == '__main__':
    main()

