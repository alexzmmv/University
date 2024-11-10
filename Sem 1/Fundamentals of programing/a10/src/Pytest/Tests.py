import unittest
from src.board.board import *

class Board_Test(unittest.TestCase):
    def setUp(self):
        self.board = Board(3, 3)

    def test_move(self):
        self.setUp()
        self.board.move(1, 1, 'X')
        self.assertEqual(self.board.get(1, 1), 1)

    def test_move_invalid(self):
        self.setUp()
        self.board.move(1, 1, 'X')
        self.assertRaises(ValueError, self.board.move, 1, 1, 'X')

    def test_move_invalid_symbol(self):
        self.setUp()
        self.assertRaises(ValueError, self.board.move, 1, 1, 'Y')

    def test_move_invalid_coordinates(self):
        self.setUp()
        self.assertRaises(ValueError, self.board.move, 5, 5, 'X')

    def test_is_ended(self):
        self.setUp()
        self.assertFalse(self.board.is_ended())
        self.board.move(1, 1, 'X')
        self.assertTrue(self.board.is_ended())

    def test_get(self):
        self.setUp()
        self.board.move(1, 1, 'X')
        self.assertEqual(self.board.get(1, 1), 1)

    def test_compute_nearby_positions(self):
        self.setUp()
        self.board.move(1, 1, 'X')
        self.assertEqual(self.board.compute_nearby_positions(1, 1), 0)

    def test_evaluate(self):
        self.setUp()
        self.board.move(1, 1, 'X')
        self.assertEqual(self.board.evaluate(), 999)

    def test_undo_for_ai(self):
        self.setUp()
        self.board.move(0, 0, '0')
        self.board.undo_for_ai()
        self.assertEqual(self.board.get(0,0),0 )

    def test_size_of_x(self):
        self.setUp()
        self.assertEqual(self.board.size_of_x, 3)

    def test_size_of_y(self):
        self.setUp()
        self.assertEqual(self.board.size_of_y,3)