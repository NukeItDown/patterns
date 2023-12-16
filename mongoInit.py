from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['warehouse']

warehouse_collection = db['warehouse_storage']

sample_data = [
    {'name': 'Product A', 'storage_count': 10, "identifyNumber": "32432"},
    {'name': 'Product B', 'storage_count': 30, "identifyNumber": "56756"},
    {'name': 'Product C', 'storage_count': 30, "identifyNumber": "08776"},
    {'name': 'Product D', 'storage_count': 30, "identifyNumber": "54745"},
    {'name': 'Product E', 'storage_count': 30, "identifyNumber": "54654"},
    {'name': 'Product F', 'storage_count': 30, "identifyNumber": "23454"},
    {'name': 'Product G', 'storage_count': 30, "identifyNumber": "17982"},
]

warehouse_collection.insert_many(sample_data)

print('Warehouse collection created and populated')
