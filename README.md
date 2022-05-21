# Verbs and Nouns finder
This simple script is designed to scrap a webpage's text contents and find all the verbs and nouns.  
For usage, type __./finder.py -h__

## External Packages Used
- beautiful soup 4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - For webscraping. 
- nltk: https://www.nltk.org/
    - Tokenizing and POS Tagging
- contractions: https://pypi.org/project/contractions/
    - Fix words like can't, don't

For fast installation of packages, use __utils/get_lib.cmd__

## NLTK data used
- punkt tokenizer
- averaged_perceptron_tagger

To download all data required, use __utils/get_nltk_data.py__