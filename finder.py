import argparse
from pydoc import describe
import sys
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import contractions
import string
import csv


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Scrap and Process Webpage Text')
    parser.add_argument("target")
    parser.add_argument("-l","--lower",action="store_true",help="Turn all words to Lower Case")
    parser.add_argument("-s","--stem",action="store_true",help="Stem all words. (Example: connects, connecting, connected --> connect)")
    parser.add_argument("-o","--output",action="store",help="Specify output file. Default to './output.csv'")

    arg_dict = vars(parser.parse_args(args))
    # print("args: ", args)
    # print("arg_dict: ", arg_dict)

    raw_text = get_text(arg_dict["target"])
    words = process_text(raw_text,lower=arg_dict["lower"],stem=arg_dict["stem"])
    print("%s words found." % len(words))
    output = arg_dict["output"] or "./output.csv"
    print("Saving Output to %s" % output)
    with open(output,"w") as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerow(words)
    
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_text(target):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(target,headers=hdr)
    page = urlopen(req)
    #html = urllib.request.urlopen('https://www.theregister.com/2022/03/11/intel_software_expansion/').read()
    return text_from_html(page)

def process_text(raw_text, lower=False, stem=False):
    expanded_raw_text = contractions.fix(raw_text)
    nltk.data.path.append("./nltk_data")
    sentences = sent_tokenize(expanded_raw_text)
    tokens = sum([nltk.word_tokenize(s) for s in sentences],[])
    words = [t for t in tokens if t.isalpha()]
    if lower:
        words = [w.lower() for w in words]
    if stem:
        snow_stemmer = SnowballStemmer(language="english")
        words = [snow_stemmer.stem(w) for w in words]
    words = list(set(words))
    words_with_pos = nltk.pos_tag(words) # better if can combine with N-Gram taggers
    # print("%s words found" % len(words))
    # print("words_with_pos",words_with_pos)
    # print("list of POS tagged",[x[1] for x in words_with_pos])
    verbs_and_nouns = [x[0] for x in words_with_pos if x[1][0] in ('N', 'V')] #
    # print("verbs_and_nouns", verbs_and_nouns)
    return verbs_and_nouns

if __name__ == "__main__":
    main()