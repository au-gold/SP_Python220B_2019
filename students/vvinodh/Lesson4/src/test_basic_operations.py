"""Unit test for basic operations program"""
# pylint: disable=W0614, C0103, W0401
import sys
from unittest import TestCase
from customer_model import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers
from basic_operations import display_customers

sys.path.append(r"C:\UW-Python-Advanced\SP_Python220B_2019\students\vvinodh\Lesson4\src")

# create a set of customers
user_1 = {'customer_id': '9990', 'name': 'Vinodh', 'lastname': 'Babuji',
          'home_address': '1900 Turnberry CT', 'phone_number': '4692201000',
          'email_address': 'vinodhbabuji@gmail.com', 'status': True,
          'credit_limit': 3000.00}

user_2 = {'customer_id': '9991', 'name': 'Suresh', 'lastname': 'Raj',
          'home_address': '1119 North way Dr', 'phone_number': '4692201001',
          'email_address': 'howardmoon@gmail.com', 'status': False,
          'credit_limit': 5000.00}

user_3 = {'customer_id': '9992', 'name': 'Paneer', 'lastname': 'Morvam',
          'home_address': '2234 Flannel PL', 'phone_number': '4692201002',
          'email_address': 'vincenoir@gmail.com', 'status': True,
          'credit_limit': 6000.00}


def drop_db():
    """Drops customer table"""
    database.drop_tables([Customer])
    database.close()


def create_empty_db():
    """Creates an empty customer database"""
    drop_db()
    database.create_tables([Customer])
    database.close()



class BasicOperationsTest(TestCase):
    """Tests basic_operations program, along with customer_model"""
    def test_add_customer(self):
        """Tests if a new customer is added to database"""
        create_empty_db()
        add_customer(**user_1)
        query = Customer.get(Customer.customer_id == user_1['customer_id'])
        self.assertEqual(user_1['name'], query.customer_name)
        self.assertEqual(user_1['lastname'], query.customer_last_name)
        self.assertEqual(user_1['home_address'], query.customer_address)
        self.assertEqual(user_1['phone_number'], query.customer_phone)
        self.assertEqual(user_1['email_address'], query.customer_email)
        self.assertEqual(user_1['status'], query.customer_status)
        self.assertEqual(user_1['credit_limit'], query.customer_limit)

        # add another person
        add_customer(**user_2)
        query = Customer.get(Customer.customer_id == user_2['customer_id'])
        self.assertEqual(user_2['name'], query.customer_name)
        self.assertEqual(user_2['lastname'], query.customer_last_name)
        self.assertEqual(user_2['home_address'], query.customer_address)
        self.assertEqual(user_2['phone_number'], query.customer_phone)
        self.assertEqual(user_2['email_address'], query.customer_email)
        self.assertEqual(user_2['status'], query.customer_status)
        self.assertEqual(user_2['credit_limit'], query.customer_limit)

        # add a duplicate person
        with self.assertRaises(ValueError):
            add_customer(**user_2)
        drop_db()

    def test_search_customer(self):
        """Tests customer search function"""
        create_empty_db()
        add_customer(**user_1)
        test_map = {'name': user_1['name'], 'lastname': user_1['lastname'],
                    'email': user_1['email_address'],
                    'phone_number': user_1['phone_number']}
        self.assertEqual(test_map, search_customer(user_1['customer_id']))

        # Non-existant Customer Test
        self.assertEqual({}, search_customer('99999'))
        drop_db()

    def test_delete_customer(self):
        """Tests if user can delete customer(s)"""
        create_empty_db()
        add_customer(**user_1)
        delete_customer(user_1['customer_id'])
        self.assertEqual({}, search_customer(user_1['customer_id']))
        drop_db()

    def test_update_customer_credit(self):
        """Tests if customer credit is updated properly"""
        create_empty_db()
        add_customer(**user_1)
        update_customer_credit(user_1['customer_id'], 5000.00)
        query = Customer.get(Customer.customer_id == user_1['customer_id'])
        self.assertEqual(5000.00, query.customer_limit)

        # Test for non-existant customer
        with self.assertRaises(ValueError):
            update_customer_credit('456879', 5000.00)

        # Test for non-float value inputted
        with self.assertRaises(TypeError):
            update_customer_credit(user_1['customer_id'], '$20')
        drop_db()

    def test_list_active_customers(self):
        """Tests list of active customers"""
        create_empty_db()
        add_customer(**user_1)
        add_customer(**user_2)
        add_customer(**user_3)
        self.assertEqual(2, list_active_customers())
        drop_db()

    def test_display_customers(self):
        """Tests the display of all customers in database"""
        create_empty_db()
        self.assertEqual([], display_customers())
        add_customer(**user_1)
        add_customer(**user_2)
        add_customer(**user_3)
        self.assertEqual(['Vinodh Babuji', 'Suresh Raj', 'Paneer Morvam'],
                         display_customers())
        drop_db()
