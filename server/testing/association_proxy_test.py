from app import app
from models import db, Customer, Item, Review

class TestAssociationProxy:
    '''Customer in models.py has association proxy to items'''

    @classmethod
    def setup_class(cls):
        """Set up the app context and create tables before running tests."""
        cls.app = app
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()  # ✅ Ensure tables exist before tests run

    @classmethod
    def teardown_class(cls):
        """Remove session and clean up after all tests."""
        db.session.remove()
        db.drop_all()  # ✅ Remove tables after tests
        cls.ctx.pop()

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with self.app.app_context():  # ✅ Ensure we're inside the app context
            customer = Customer(name="Test Customer")
            item = Item(name="Test Item", price=10.0)
            db.session.add_all([customer, item])
            db.session.commit()

            review = Review(comment="Great!", customer_id=customer.id, item_id=item.id)
            db.session.add(review)
            db.session.commit()

            # Check if the association proxy works
            assert customer.items == [item]
