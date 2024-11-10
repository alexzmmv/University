import unittest
from src.repository.MemoryRepo import MemoryRepository, Repository_error
import datetime
import coverage


class TestMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repo = MemoryRepository()

    def test_add_person(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.assertIn(1, self.repo.persons)

    def test_add_person_duplicate_id(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        with self.assertRaises(Repository_error):
            self.repo.add_person(1, "Jane Doe", "987-654-3210")

    def test_update_person(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.update_person(1, "Jane Doe", "987-654-3210")
        person = self.repo.get_person_by_id(1)
        self.assertEqual(person.name, "Jane Doe")
        self.assertEqual(person.phone_number, "987-654-3210")

    def test_update_person_nonexistent_id(self):
        with self.assertRaises(Repository_error):
            self.repo.update_person(1, "Jane Doe", "987-654-3210")

    def test_add_activity(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.add_activity(1, [1], "2023.01.01", "10:00", "12:00", "Example Activity")
        self.assertIn(1, self.repo.activities)

    def test_add_activity_duplicate_id(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.add_activity(1, [1], "2023.01.01", "10:00", "12:00", "Example Activity")
        with self.assertRaises(Repository_error):
            self.repo.add_activity(1, [1], "2023.01.01", "14:00", "16:00", "Another Activity")

    def test_update_activity(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.add_activity(1, [1], "2023.01.01", "10:00", "12:00", "Example Activity")
        self.repo.update_activity(1, [1], "2023.01.01", "14:00", "16:00", "Updated Activity")
        activity = self.repo.get_activity_by_id(1)
        self.assertEqual(activity.description, "Updated Activity")
        expected_start_time = datetime.datetime.strptime("14:00", "%H:%M")
        self.assertEqual(activity.start_time, expected_start_time)

    def test_update_activity_nonexistent_id(self):
        with self.assertRaises(Repository_error):
            self.repo.update_activity(1, [1], "2023.01.01", "14:00", "16:00", "Updated Activity")

    def test_delete_person(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.delete_person(1)
        self.assertNotIn(1, self.repo.persons)

    def test_delete_person_nonexistent_id(self):
        with self.assertRaises(Repository_error):
            self.repo.delete_person(1)

    def test_delete_activity(self):
        self.repo.add_person(1, "John Doe", "123-456-7890")
        self.repo.add_activity(1, [1], "2023.01.01", "10:00", "12:00", "Example Activity")
        self.repo.delete_activity(1)
        self.assertNotIn(1, self.repo.activities)

    def test_delete_activity_nonexistent_id(self):
        with self.assertRaises(Repository_error):
            self.repo.delete_activity(1)