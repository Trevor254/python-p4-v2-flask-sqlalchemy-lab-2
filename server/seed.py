from app import app
from models import db, Customer, Item, Review

with app.app_context():
    print("Creating tables...")
    db.create_all()  # ✅ Ensures tables exist before running queries

    print("Deleting old records...")
    db.session.query(Customer).delete()
    db.session.query(Item).delete()
    db.session.query(Review).delete()
    
    # Add new data
    print("Seeding data...")
    customer1 = Customer(name="John Doe")
    item1 = Item(name="Laptop", price=1200.00)

    db.session.add(customer1)
    db.session.add(item1)
    db.session.commit()

    review1 = Review(comment="Great product!", customer_id=customer1.id, item_id=item1.id)
    db.session.add(review1)
    db.session.commit()

    print("Seeding complete!")