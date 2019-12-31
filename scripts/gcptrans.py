# Imports the Google Cloud client library
import os
import time
from google.cloud import translate_v2 as translate
from retrying import retry

"""
export GOOGLE_APPLICATION_CREDENTIALS="<path to json file with credentials>"
"""

class Translator():

	def __init__(self, target_language):
		self.target = target_language
		self.client = translate.Client()

	@retry(stop_max_attempt_number=7)
	def translate(self, text):
		translation = self.client.translate(text, target_language=self.target, format_="text")
		return self.format(translation['translatedText'])

	def format(self, translated_text):
		translated_text = translated_text.replace('&#39;', "'")
		translated_text = translated_text.replace('&quot;', "'")
		return translated_text
