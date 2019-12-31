from ebook import Ebook
from gcptrans import Translator
import json
from text_tokenizer import TextTokenizer
import argparse
import csv
import argparse
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser(
    description='Missing arguments --input <path>.txt --output <path>.html --lang <locale>')
parser.add_argument('--input', metavar='N', type=str, nargs='+',
                    help='path to infile txt')
parser.add_argument('--lang', metavar='N', type=str, nargs='+',
                    help='path outfile html')

args = parser.parse_args()


assert args.input and args.lang, parser.description

path = args.input[0]
text = Ebook(path).sentences
translator = Translator(args.lang[0])
enumerated_sentences = [{"index": index, "sentence": sentence} for index, sentence in enumerate(text)]


def translate(sen_dict):
    global total
    translated = translator.translate(sen_dict["sentence"])
    print(round(sen_dict["index"] / total * 100, 2), r"%")
    return {"index": sen_dict["index"], "original": sen_dict["sentence"], "translated": translated}


pool = ThreadPool(20)
global total
total = len(text)
results = pool.map(translate, enumerated_sentences)

df = pd.DataFrame(results)
del df["index"]
df.to_csv(path.replace(".txt", ".csv"), index=False)
df = df.replace('\n', '<br>', regex=True)
df.to_html(path.replace(".txt", ".html"), index=False, border=0, header=False, escape=False)

pool.close()
pool.join()
