"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows,bcrypt

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data



class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        # Create the Flask app
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

        # Set up the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create the database tables
        db.create_all()


        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        self.u1 = u1
        self.u2 = u2

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        """Clean up the database and application context."""

        # Remove the database tables
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.app_context.pop()


    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.followers), 0)

        # Assert that the __repr__ method returns the expected string
        self.assertEqual(repr(self.u1),f"<User #{self.u1.id}: testuser, test@test.com>")

    def test_is_following(self):
        '''testing is_following unit test'''
        self.assertFalse(self.u1.is_following(self.u2))
        self.assertFalse(self.u1.is_followed_by(self.u1))


        # u1 follows u2
        user = Follows(user_being_followed_id=self.u2.id,user_following_id=self.u1.id)
        db.session.add(user)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertTrue(self.u2.is_followed_by(self.u1))
    
    def test_signup(self):
        """Test the signup method of the User model."""

        # Call the signup method to create a new user
        user = User.signup(
            username="testSignUp",
            email="testSignUp@test.com",
            password="password",
            image_url="/path/to/image"
        )
        db.session.commit()

        # Retrieve the user from the database
        db_user = User.query.filter_by(username="testSignUp").one_or_none()
        
        # Assert that the user was added to the database
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, "testSignUp")
        self.assertEqual(db_user.email, "testSignUp@test.com")
        self.assertTrue(bcrypt.check_password_hash(db_user.password,"password"))
    
    def test_sign_up_duplicate(self):
        '''User verifies Integrtiy error when enters already exsis account'''
        with self.assertRaises(IntegrityError):
            user = User.signup(
                username="testuser",
                email="test@test.com",
                password="password",
                image_url="/path/to/image"
        )
            
            db.session.commit()


    def test_authenticate(self):
        """Test the signup method of the User model."""

        # Call the signup method to create a new user
        user = User.signup(
            username="testSignUp",
            email="testSignUp@test.com",
            password="password",
            image_url="/path/to/image"
        )
        db.session.commit()

        # If wrong username or password pass validate False
        self.assertFalse(user.authenticate("testSignUp","12312"))
        self.assertFalse(user.authenticate("x","password"))

        
        # if password correct check return user 
        self.assertEqual(user,user.authenticate("testSignUp","password"))







        
        





