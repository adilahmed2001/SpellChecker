import requests

def get_response(word):
    url = f'enter spell check URL={word}'
    
    return requests.get(url).text

def parse_text(response):
	return response == 'true'

def spell_check(word):
	return parse_text(get_response(word))
