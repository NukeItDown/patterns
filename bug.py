from settings import db, app
from models import Product, similar_products

with app.app_context():
    sample_products_data = [
        {'name': 'Product 1', 'price': 19.99},
        {'name': 'Product 2', 'price': 29.99},
        {'name': 'Product 3', 'price': 39.99}
    ]

    for product_data in sample_products_data:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()

    product1 = Product.query.filter_by(name='Product 1').first()
    product2 = Product.query.filter_by(name='Product 2').first()
    product3 = Product.query.filter_by(name='Product 3').first()

    similar_products_data = [
        {'product_id': product1.id, 'similar_id': product2.id},
        {'product_id': product1.id, 'similar_id': product3.id}
    ]

    for relationship_data in similar_products_data:
        product_id = relationship_data['product_id']
        similar_id = relationship_data['similar_id']

        similar_relationship = SimilarProducts(product_id=product_id, similar_id=similar_id)
        db.session.add(similar_relationship)

    db.session.commit()
    print("success")


MGoClient = MongoClient('mongodb://localhost:27017')

database = MGoClient["warehouse"]
collection = database["warehouse_storage"]

for mongo_product in mongo_products:
    if not Product.query.filter_by(indetifynumber=collection['identifyNumber']).first():
        new_product = Product(name=mongo_product['name'], price=mongo_product['price'], identifynumber=mongo_product['identifyNumber'])
        db.session.add(new_product)

db.session.commit()