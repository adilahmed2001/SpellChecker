from src.documentspellchecker import *
import unittest
from unittest.mock import Mock
from textwrap import dedent

class DocumentSpellCheckerTests(unittest.TestCase):
	def test_canary(self):
		self.assertTrue(True)

	def test_text_empty(self):
		check_spelling = Mock(return_value=True)

		self.assertEqual('', process_text('', check_spelling))

	def test_text_has_no_spelling_mistakes(self):
		check_spelling = Mock(return_value=True)

		self.assertEqual('hello', process_text('hello', check_spelling))

	def test_text_has_incorrect_spelling_blah(self):
		check_spelling = Mock(return_value=False)

		self.assertEqual('[blah]', process_text('blah', check_spelling))
  
	def test_text_has_no_spelling_mistakes_and_two_words(self):
		check_spelling = Mock(return_value=True)

		self.assertEqual('hello there', process_text('hello there', check_spelling))

	def test_text_has_one_spelling_mistake_and_two_words(self):
		check_spelling = Mock(side_effect = lambda word: word != 'misp')

		self.assertEqual('hello [misp]', process_text('hello misp', check_spelling))
	
	def test_text_has_two_spelling_mistakes_and_multiple_words(self):
		check_spelling = Mock(side_effect = lambda word: word not in ['misp', 'tyop'])

		self.assertEqual('hello [tyop] there [misp]', process_text('hello tyop there misp', check_spelling))

	def test_text_has_two_lines_no_spelling_mistakes(self):
		check_spelling = Mock(return_value=True)
		
		input_text = dedent(
							"""\
								Hello World
								How are you"""
							)

		self.assertEqual(input_text, process_text(input_text, check_spelling))
 

	def test_text_has_two_lines_with_spelling_mistakes(self):
		check_spelling = Mock(side_effect = lambda word: word not in ['Wor', 're'])

		output_text = dedent(
							"""\
								Hello [Wor]
								How [re] you"""
							)

		input_text = dedent(
							"""\
								Hello Wor
								How re you"""
							)
	
		self.assertEqual(output_text, process_text(input_text, check_spelling))
		
	def test_text_has_three_lines_no_spelling_mistakes(self):
		check_spelling = Mock(return_value=True)

		input_text = dedent(
							"""\
								Hello World
								How are you
								That is great"""
							)

		self.assertEqual(input_text, process_text(input_text, check_spelling))

	def test_text_has_three_lines_with_spelling_mistakes(self):
		check_spelling = Mock(side_effect = lambda word: word not in ['Wor', 're', 'iss'])

		input_text = dedent(
							"""\
								Hello Wor
								How re you
								That iss great"""
							)

		output_text = dedent(
							"""\
								Hello [Wor]
								How [re] you
								That [iss] great"""
							)

		self.assertEqual(output_text, process_text(input_text, check_spelling))

	def test_process_text_runs_into_one_exception(self):

		def check_spelling_side_effect(word):
			if word == 'there':
				raise Exception()
			return True

		check_spelling = Mock(side_effect = check_spelling_side_effect)

		self.assertEqual('hello ?there? how aare you', process_text('hello there how aare you', check_spelling))

	def test_process_text_has_one_spelling_mistake_two_exceptions(self):

		def check_spelling_side_effect(word):
			if word in ['there', 'aare']:
				raise Exception()

			return word != 'hwo'

		check_spelling = Mock(side_effect = check_spelling_side_effect)

		self.assertEqual('hello ?there? [hwo] ?aare? you', process_text('hello there hwo aare you', check_spelling))


	def test_process_text_has_three_lines_multiple_spelling_mistakes_multiple_exceptions(self):

		input_text = dedent(
							"""\
								Hello Wor
								How re yours
								That iss great to hears from yours"""
							)

		output_text = dedent(
							"""\
								Hello [Wor]
								How [re] ?yours?
								That [iss] great to ?hears? from ?yours?"""
							)

		def check_spelling_side_effect(word):
			if word in ['yours', 'hears', 'yours']:
				raise Exception()

			return word not in ['Wor', 'iss', 're']

		check_spelling = Mock(side_effect = check_spelling_side_effect)

		self.assertEqual(output_text, process_text(input_text, check_spelling))
