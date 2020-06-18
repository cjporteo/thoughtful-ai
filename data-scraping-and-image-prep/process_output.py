import os
import sqlite3
import random
import sys

sys.path.append('../gpt-2-simple')

import generate

def filter_quote(quote, db_list):
    
    if len(quote) <= 25 or len(quote) > 140:
        return False
    if any(quote.strip('“”.') in x for x in db_list):
        return False

    blacklist_words = [
            'god',
            'lord'
            'jesus',
            'man',
            'woman'
            'suicide',
            'fuck',
            'shit',
            'rape'
        ]

    if any(blw in quote.lower() for blw in blacklist_words):
        return False

    return True

def get_quote():

    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()

    c.execute(
        """
        SELECT quote 
        FROM quotes
        """
    )

    quotes_in_db = []

    for row in c:
        quotes_in_db.append(row[0])

    #print(len(quotes_in_db))

    attempts = 0
    sess = None

    while True:

        os.chdir('../gpt-2-simple')
        sess = generate.attempt_generate(sess)
        os.chdir('../data-scraping-and-image-prep')

        files = []
        for file in os.listdir('model-output'):
            files.append(file)
        file = sorted(files, reverse=True)[0]

        #print('Reading from: ' + file, end='\n\n')

        model_output = None

        with open('model-output/' + file, 'r') as f:
            model_output = f.read()

        quote_candidates = model_output.split('<|endoftext|>')[1:-1]

        quote_candidates = [x for x in quote_candidates if filter_quote(x, quotes_in_db)]
        '''
        for qc in quote_candidates:
            print(qc, end='\n\n')
        '''

        if len(quote_candidates) > 0:
            return random.choice(quote_candidates)

        attempts += 1
        if attempts > 5:
            return """“I have discovered a truly marvelous demonstration 
            of wisdom that this margin is too narrow to contain.”"""