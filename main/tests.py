from django.test import TestCase
from main.models import Board

# Create your tests here.
class BoardTest(TestCase):
    def setUp(self):
        Board.objects.create(board_id="pup", name="Polytecnic Universitiy of The Philippines")

    def test_get_board(self):
        board = Board.objects.get(board_id='pup')
        self.assertEqual(board.board_id, 'pup')