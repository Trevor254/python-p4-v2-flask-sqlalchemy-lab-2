from app import app
from models import db, Customer, Item, Review

class TestSerialization:
    '''models in models.py are serializable'''

    @classmethod
    def setup_class(cls):
        """Set up the app context and create tables before running tests."""
        cls.app = app
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()  # ✅ Ensures tables exist before tests run

    @classmethod
    def teardown_class(cls):
        """Remove session and clean up after all tests."""
        db.session.remove()
        db.drop_all()  # ✅ Remove tables after tests
        cls.ctx.pop()

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with self.app.app_context():  # ✅ Ensure we're inside the app context
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()

            serialized = c.to_dict()
            assert 'name' in serialized
            assert serialized['name'] == 'Phil'

    def test_item_is_serializable(self):
        '''item is serializable'''
        with self.app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()

            serialized = i.to_dict()
            assert 'name' in serialized
            assert 'price' in serialized
            assert serialized['name'] == 'Insulated Mug'

    def test_review_is_serializable(self):
        '''review is serializable'''
        with self.app.app_context():
            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=10.0)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='Great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            serialized = r.to_dict()
            assert 'comment' in serialized
            assert serialized['comment'] == 'Great!'