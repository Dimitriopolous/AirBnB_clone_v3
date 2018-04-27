#!/usr/bin/python3
''' Unit tests for DB storage '''
import os
import unittest
import models
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Only want to test Database storage")
class testDBStorage(unittest.TestCase):
    '''
    Testing the DB storage class
    '''
    def test_existence_user(self):
        '''
        Testing if User class is being created properly
        '''
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        if user.id in models.storage.all('User'):
            self.assertTrue(user.password, "johnpwd")

    def test_existence_amenity(self):
        '''
        Testing if Amenity class is being created properly
        '''
        amenity = Amenity(name="Wifi")
        amenity.save()
        if amenity.id in models.storage.all():
            self.assertTrue(amenity.name, "Wifi")

    def test_existence_state(self):
        '''
        Testing if State class is being created properly
        '''
        state = State(name="Alaska")
        state.save()
        if state.id in models.storage.all():
            self.assertTrue(state.name, "Alaska")

    def test_all_method(self):
        '''
        Testing if all() method returns all instances
        '''
        state = State(name="Cali")
        state.save()
        amenity = Amenity(name="Cable")
        amenity.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        test_me = str(state.id) + str(amenity.id) + str(user.id)
        if test_me in models.storage.all():
            self.assertTrue(state.name, "Cali")

    def test_delete_method(self):
        '''
        Tests the delete method in db_storage
        '''
        state = State(name="Texas")
        state.save()
        all_stored = models.storage.all()
        models.storage.delete(state)
        self.assertTrue(all_stored["State." + state.id])

    def test_get_count_no_string(self):
        '''
        Tests if cls is not a string in the get() and count() methods
        '''
        state = State(name="California")
        state.save()
        count = len(models.storage.all())
        got = models.storage.get('', state.id)
        self.assertEqual(got, None)
        got_id = models.storage.get(state.__class__.__name__, '')
        self.assertEqual(got_id, None)
        counted = models.storage.count('')
        self.assertEqual(counted, count)

    def test_get_not_strings(self):
        '''
        Testing get() method if passed with incorrect type
        '''
        state = State(name="Arizona")
        state.save()
        got_name = models.storage.get(5, state.id)
        got_id = models.storage.get(state.__class__.__name__, 6)
        self.assertEqual(got_name, None)
        self.assertEqual(got_id, None)

    def test_count_not_string(self):
        '''
        Testing count() method if passed with incorrect type
        '''
        self.assertRaises(TypeError, models.storage.count(5))

    def test_class_id_not_exists(self):
        '''
        Testing get() and count() functions for non-existent classes
        '''
        state = State(name="California")
        state.save()
        self.assertRaises(NameError, lambda: models.storage.get("Food",
                                                                state.id))
        self.assertEqual(models.storage.get(state.__class__.__name__,
                                            "1234-5678"), None)
        self.assertRaises(NameError, lambda: models.storage.count("Food"))

    def test_correct_output(self):
        '''
        Testing get and count for correct output
        '''
        state = State(name="Oregon")
        state.save()
        self.assertEqual(models.storage.count("State"),
                         len(models.storage.all("State")))

    def test_too_many_args(self):
        '''
        Testing get() and count() methods if too many args are passed
        '''
        state = State(name="Hawaii")
        state.save()
        self.assertRaises(TypeError,
                          lambda: models.storage.count("State", "extra"))
        first_state_id = list(models.storage.all("State").values())[0].id
        self.assertRaises(TypeError, lambda: models.storage.get("State",
                          first_state_id, "extra"))

    def test_zero_args(self):
        '''
        Testing get() and count() methods if no args are passed
        '''
        state = State(name="Hawaii")
        state.save()
        self.assertEqual(len(models.storage.all()), models.storage.count())
        first_state_id = list(models.storage.all("State").values())[0].id
        self.assertRaises(TypeError, lambda: models.storage.get())

if __name__ == '__main__':
    unittest.main()
