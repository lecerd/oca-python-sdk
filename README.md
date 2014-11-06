OCA Python SDK
==============

Python SDK for OCA's [OEP Tracking](http://webservice.oca.com.ar/oep_tracking/) app.

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

POSTAL_CODE = 'XXXX'
OPERATIVE = 'XXXXX'
TRACKING_NUMBER = 'XXXXXXXXXXXXXXXXXXX'

oca = OCA(CLIENT_CUIT)

province_list = oca.get_province_list()
province = province_list[0]
province_districts = oca.get_district_list_by_province(province['province_id'])

imposition_centers = oca.get_imposition_center_list()
imposition_centers_for_postal_code = oca.get_imposition_center_list_by_postal_code(POSTAL_CODE)

admision_centers = oca.get_admission_center_list()
admision_centers_for_postal_code = oca.get_admission_center_list_by_postal_code(POSTAL_CODE)

shipping = {
    'operative': OPERATIVE,
    'weight': '1', #kg
    'volume': '0.005', #m3
    'package_count': '1',
    'postal_code_from': CLIENT_POSTAL_CODE,
    'postal_code_to': POSTAL_CODE
}

shipping_cost = oca.get_shipping_cost(**shipping)
shipping_status = oca.get_shipping_status(TRACKING_NUMBER)
```

Dependencies
------------

* [requests](http://github.com/kennethreitz/requests)
* [lxml](http://github.com/lxml/lxml)

Version
-------

0.1.0


License
-------

MIT
