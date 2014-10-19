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
```
shipping_data = {
    'operative': '',
    'weight': '',
    'volume': '',
    'postal_code_from': '',
    'postal_code_to': '',
    'package_count': ''
}
```

Version
-------

0.1.0


License
-------

MIT
