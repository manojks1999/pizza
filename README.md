# pizza

## How to run application.
1. Get a clone
2. run: docker compose up

## Desing

The system has 3 APIS

1. Menu [GET]
2. Place Order [POST]
3. Track Order [GET]

1. Menu API [GET]
http://127.0.0.1:5000/api/menu
Response:
```
{
    "data": {
        "base": [
            {
                "id": "715e4f75-4a38-11ee-bb37-02001709d070",
                "name": "Thin Crust",
                "price": 500
            },
            {
                "id": "717c7399-4a38-11ee-bb37-02001709d070",
                "name": "Normal",
                "price": 400
            },
            {
                "id": "7195231e-4a38-11ee-bb37-02001709d070",
                "name": "Cheese Burst",
                "price": 200
            }
        ],
        "cheese": [
            {
                "id": "73536cd6-4a38-11ee-bb37-02001709d070",
                "name": "Mozzarella Cheese",
                "price": 20
            },
            {
                "id": "73893a00-4a38-11ee-bb37-02001709d070",
                "name": "Provolone Cheese",
                "price": 30
            },
            {
                "id": "73b95aab-4a38-11ee-bb37-02001709d070",
                "name": "Cheddar Cheese",
                "price": 15
            },
            {
                "id": "73eeeac3-4a38-11ee-bb37-02001709d070",
                "name": "Gouda",
                "price": 45
            }
        ],
        "topping": [
            {
                "id": "71e64534-4a38-11ee-bb37-02001709d070",
                "name": "Marinara sauce",
                "price": 20
            },
            {
                "id": "721ce83f-4a38-11ee-bb37-02001709d070",
                "name": "Chicken breast",
                "price": 30
            },
            {
                "id": "724e862e-4a38-11ee-bb37-02001709d070",
                "name": "Green peppers",
                "price": 15
            },
            {
                "id": "728422bb-4a38-11ee-bb37-02001709d070",
                "name": "Black olives",
                "price": 45
            },
            {
                "id": "72b730c5-4a38-11ee-bb37-02001709d070",
                "name": "Spinach",
                "price": 20
            },
            {
                "id": "72f02160-4a38-11ee-bb37-02001709d070",
                "name": "Mushrooms",
                "price": 15
            },
            {
                "id": "732131c6-4a38-11ee-bb37-02001709d070",
                "name": "Onions",
                "price": 10
            }
        ]
    },
    "success": true
}
```

2. Place Order. [POST]

http://127.0.0.1:5000/api/order

Payload:
Place the item id from menu api.
1 base
1 cheese
5 toppings

Can make multiple order in same api by adding as list
Once the order place the status is changed as requirements asynchronously with celery.

After 1 minute, the status should change from ‘Accepted’ to ‘Preparing’
After 3 minutes it should change from ‘Preparing’ to ‘Dispatched’
After 5 minutes it should read ‘Delivered’
```
{
    "data": [
        {
            "base": "715e4f75-4a38-11ee-bb37-02001709d070",
            "cheese": "73536cd6-4a38-11ee-bb37-02001709d070",
            "topping": [
                "71e64534-4a38-11ee-bb37-02001709d070",
                "721ce83f-4a38-11ee-bb37-02001709d070",
                "724e862e-4a38-11ee-bb37-02001709d070",
                "728422bb-4a38-11ee-bb37-02001709d070",
                "72b730c5-4a38-11ee-bb37-02001709d070"
            ]
        }
    ]
}
```
Response:

```
{
    "order_id": "41c17c71-028d-4d5d-b1d2-8424af86aa5a",
    "success": true
}
```

3. Track Order [GET]

http://127.0.0.1:5000/api/order?order_id=<order_id>
Example: http://127.0.0.1:5000/api/order?order_id=41c17c71-028d-4d5d-b1d2-8424af86aa5a

Response:

```
{
    "data": {
        "id": "41c17c71-028d-4d5d-b1d2-8424af86aa5a",
        "items": [
            {
                "base": "Thin Crust",
                "cheese": "Mozzarella Cheese",
                "price": 650,
                "topping": [
                    "Marinara sauce",
                    "Chicken breast",
                    "Green peppers",
                    "Black olives",
                    "Spinach"
                ]
            }
        ],
        "ordered_at": "Sun, 03 Sep 2023 11:03:33 GMT",
        "price": 650.0,
        "quantity": 1,
        "status": "Accepted",
        "updated_at": "Sun, 03 Sep 2023 11:03:43 GMT"
    },
    "success": true
}
```
