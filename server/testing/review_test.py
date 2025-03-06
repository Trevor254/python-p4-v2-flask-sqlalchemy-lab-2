from app import create_app
from models import db, Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    @classmethod
    def setup_class(cls):
        """Set up the app context and create tables before running tests."""
        cls.app = create_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()  # ✅ Ensure tables exist before tests run

    @classmethod
    def teardown_class(cls):
        """Remove session and clean up after all tests."""
        db.session.remove()
        db.drop_all()  # ✅ Remove tables after tests
        cls.ctx.pop()

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with self.app.app_context():  # ✅ Use the test app context
            customer = Customer(name="Test Customer")
            item = Item(name="Test Item", price=10.0)
            db.session.add(customer)
            db.session.add(item)
            db.session.commit()

            review = Review(comment='great!', customer_id=customer.id, item_id=item.id)
            db.session.add(review)
            db.session.commit()

            saved_review = Review.query.filter_by(comment='great!').first()
            assert saved_review is not None
            assert saved_review.customer_id == customer.id
            assert saved_review.item_id == item.id

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with self.app.app_context():  # ✅ Use the test app context
            customer = Customer(name="Test Customer 2")
            item = Item(name="Test Item 2", price=15.0)
            db.session.add_all([customer, item])
            db.session.commit()

            review = Review(comment='great!', customer=customer, item=item)
            db.session.add(review)
            db.session.commit()

            assert review.customer_id == customer.id
            assert review.item_id == item.id
            assert review.customer == customer
            assert review.item == item
            assert review in customer.reviews
            assert review in item.reviews