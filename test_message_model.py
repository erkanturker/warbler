"""Message model tests."""

import os
from unittest import TestCase
from app import app
from models import db, User, Message, Follows,bcrypt

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

class MessageModelTestCase(TestCase):
     """Test message for messages."""
     def setUp(self):

        # Create the Flask app
        app.config['TESTING'] = True
        app.config['D EBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

        # Set up the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create the database tables
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        # Call the signup method to create a new user
        user = User.signup(
            username="testSignUp",
            email="testSignUp@test.com",
            password="password",
            image_url="/path/to/image"
        )
        db.session.commit()
        self.user = user

         # Create a test client
        self.client = app.test_client()

     def tearDown(self):
        """Clean up the database and application context."""

        # Remove the database tables
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.app_context.pop()
    
     def test_message(self):
         message = Message(text="This is Message",user_id=self.user.id)
         db.session.add(message)
         db.session.commit()

         self.assertEqual(len(self.user.messages),1)
         self.assertEqual(self.user.messages[0].text,"This is Message")



    









