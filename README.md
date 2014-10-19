OCA Python SDK
==============

Python SDK for OCA's "OCA Express Pak"


Methods
-------

##### get_province_list()
##### get_district_list_by_province(province_id)
##### get_imposition_center_list()
##### get_imposition_center_list_by_postal_code(postal_code)
##### get_admission_center_list()
##### get_admission_center_list_by_postal_code(postal_code)
##### get_shipping_status(tracking_number)
##### get_shipping_cost(**shipping_data)


Usage
-----

```
from oca_sdk import OCA

CLIENT_CUIT = 'XX-XXXXXXXX-X'
CLIENT_POSTAL_CODE = 'XXXX'

POSTAL_CODE = 'XXX'
OPERATIVE = 'XXXXX'
TRACKING_NUMBER = 'XXXXXXXXXXXXXXXXXXX'

oca = OCA(CLIENT_CUIT)

provinces = oca.get_province_list()

province = province_list[0]
province_districts = oca.get_district_list_by_province(province['provinceID'])

imposition_centers = oca.get_imposition_center_list()
imposition_centers_for_postal_code = oca.get_imposition_center_list_by_postal_code(POSTAL_CODE)

admision_centers = oca.get_admission_center_list()
admision_centers_for_postal_code = oca.get_admission_center_list_by_postal_code(POSTAL_CODE)

shipping = {
    'operative': OPERATIVE,
    'weight': '1', # kg
    'volume': '0.002', # m3
    'package_count': '1',
    'postal_code_from': CLIENT_POSTAL_CODE,
    'postal_code_to': POSTAL_CODE
}

shipping_cost = oca.get_shipping_cost(**shipping)
shipping_status = oca.get_shipping_status(TRACKING_NUMBER)
```

Version
-------

0.1.0


License
-------

MIT
