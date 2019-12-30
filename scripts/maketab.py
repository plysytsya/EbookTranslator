from ebook import Ebook
from gcptrans import Translator
import json
from text_tokenizer import TextTokenizer
import argparse
import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
	description='Missing arguments --input <path>.txt --output <path>.html --lang <locale>')
parser.add_argument('--input', metavar='N', type=str, nargs='+',
                    help='path to infile txt')
parser.add_argument('--output', metavar='N', type=str, nargs='+',
                    help='path outfile html')
parser.add_argument('--lang', metavar='N', type=str, nargs='+',
                    help='path outfile html')

args = parser.parse_args()

assert args.input and args.output and args.lang, parser.description

path = args.input[0]
text = Ebook(path).sentences
translator = Translator(args.lang[0])
with open(path.replace(".txt", ".csv"), "w") as f:
	writer = csv.writer(f)
	for i, es in enumerate(text):
		writer.writerow([es, str(translator.translate(es))])
		print(round(i/len(text) * 100, 2), r"%")
df = pd.read_csv(path.replace(".txt", ".csv"))
df.to_html(args.output[0], index=False, border=0, header=False)