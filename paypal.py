import json

data = """{
    "transactionData": {
        "orderID": "8X241719MD328941W",
        "id": "8X241719MD328941W",
        "status": "COMPLETED",
        "intent": "CAPTURE",
        "create_time": "2024-08-01T12:21:41Z",
        "update_time": "2024-08-01T12:21:48Z",
        "payer": {
            "name": {
                "given_name": "John",
                "surname": "Doe"
            },
            "email_address": "buyer@speed.codes",
            "payer_id": "56NTW9BN78UR8",
            "address": {
                "country_code": "DE"
            },
            "phone": null
        },
        "purchase_units": [
            {
                "reference_id": "default",
                "amount": {
                    "currency_code": "EUR",
                    "value": "14.00"
                },
                "payee": {
                    "email_address": "seller@speed.codes",
                    "merchant_id": "R9EVPB7E2LKPN"
                },
                "shipping": {
                    "name": {
                        "full_name": "John Doe"
                    },
                    "address": {
                        "address_line_1": "Badensche Str. 24",
                        "admin_area_2": "Berlin",
                        "admin_area_1": "Berlin",
                        "postal_code": "10715",
                        "country_code": "DE"
                    }
                },
                "payments": {
                    "captures": [
                        {
                            "id": "7X6692402A7736254",
                            "status": "COMPLETED",
                            "amount": {
                                "currency_code": "EUR",
                                "value": "14.00"
                            },
                            "final_capture": true,
                            "seller_protection": {
                                "status": "ELIGIBLE",
                                "dispute_categories": [
                                    "ITEM_NOT_RECEIVED",
                                    "UNAUTHORIZED_TRANSACTION"
                                ]
                            },
                            "create_time": "2024-08-01T12:21:48Z",
                            "update_time": "2024-08-01T12:21:48Z"
                        }
                    ]
                }
            }
        ],
        "links": [
            {
                "href": "https://api.sandbox.paypal.com/v2/checkout/orders/8X241719MD328941W",
                "rel": "self",
                "method": "GET"
            }
        ]
    },
    "formData": {
        "name": "rahima",
        "pickupTime": "14:21",
        "email": "shuhib_s@live.de",
        "phone": "017610000080"
    }
}"""
print(json.dumps(data, indent=4))
