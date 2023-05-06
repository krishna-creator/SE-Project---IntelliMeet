from unittest import TestCase
from flask import Flask
from flask_testing import TestCase as Ft
from app import app

class FlaskAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def test_index_page(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')
    
    def test_send_invites(self):
        # Add participant data for testing
        participant_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'ipaddress': '127.0.0.1',
            'port': '8080'
        }
        with self.client.session_transaction() as session:
            session['participants'] = [participant_data]

        response = self.client.post('/sendInvites')
        self.assert200(response)
        # Assert that the participants list is empty after sending invites
        with self.client.session_transaction() as session:
            self.assertEqual(session.get('participants'), [])

if __name__ == '__main__':
    unittest.main()