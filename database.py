from models import UserInDB

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    },
}

fake_items_db = {
    1: {
        "id": 1,
        "name": "Foo",
        "description": "The famous Foo item",
        "price": 50.2,
        "tax": 5.0,
        "owner": "johndoe",
    },
    2: {
        "id": 2,
        "name": "Bar",
        "description": "The Bar fighters",
        "price": 62.0,
        "tax": 6.2,
        "owner": "johndoe",
    },
    3: {
        "id": 3,
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 5.0,
        "owner": "alice",
    },
}