from documentspellchecker import *
from wordspellchecker import *
import sys

def read_file(file_name):
	with open(file_name, "r") as file:
		return file.read()

def spell_check_text(text):
	return process_text(text, spell_check)

def display_in_console(processed_text):
	print(processed_text)
	
display_in_console(spell_check_text(read_file(sys.argv[1])))
