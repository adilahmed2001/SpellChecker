from src.wordspellchecker import *
import unittest
from unittest.mock import Mock
from unittest.mock import patch

class WordSpellCheckerTests(unittest.TestCase):
	def test_get_response_length_greater_than_0(self):
		self.assertGreater(len(get_response('blah')), 0)

	def test_parse_text_takes_true(self):
		self.assertTrue(parse_text('true'))

	def test_parse_text_takes_False(self):
		self.assertFalse(parse_text('false'))

	@patch('src.wordspellchecker.get_response', return_value = 'true')
	@patch('src.wordspellchecker.parse_text', return_value = True)
	def test_spell_check_pass_to_get_response_pass_to_and_returns_from_parse_text(self, mock_parse_text, mock_get_response):
		word = 'ok'
		
		response = spell_check(word)
						
		mock_get_response.assert_called_once_with(word)

		mock_parse_text.assert_called_once_with('true')

		self.assertEqual(response, mock_parse_text.return_value)

	@patch('src.wordspellchecker.get_response')
	def test_spell_check_throws_exception_when_get_response_throws(self, mock_get_response):

		def get_response_side_effect(word):
				raise Exception('Something went wrong with the url')

		mock_get_response.side_effect = get_response_side_effect

		with self.assertRaisesRegex(Exception, 'Something went wrong with the url'):
				spell_check('okay')
