# -*- coding: utf-8 -*- 

from aliexpress_api_client import AliExpress
from aliexpress_api_client.config import ALIBABA_API_FIELDS


aliexpress = AliExpress('85206', 'jasperyanky', '7AC5ioXODUOm')

# r = aliexpress.get_similar_products('32767250140', language='ru')

# r = aliexpress.get_product_list(ALIBABA_API_FIELDS['list'], 'bag', pageNo=1)

# r = aliexpress.get_product_details(ALIBABA_API_FIELDS['details'], 32784533532)

r = aliexpress.get_hot_products(3, language='ru')


r = aliexpress.get_banner('all', language='ru', pageNo=2)

# 32784533532

print(r)