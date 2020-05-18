import sqlite3
import re
import os
import sys
import urllib.request
import csv
import random
from bs4 import BeautifulSoup

####################
#
####################

ITALIAN_VERB = "https://conjugator.reverso.net/conjugation-italian-verb-%s.html"
DBPATH = '/Users/davidp/work/verbe-italiani/data/db/app.db'

HTMLDATA = 'data/html'
CSVDATA = 'data/csvs'

blocks = [
    "Indicativo Presente",
    "Indicativo Imperfetto",
    "Indicativo Passato remoto",
    "Indicativo Futuro semplice",
    "Indicativo Passato prossimo",
    "Indicativo Trapassato prossimo",
    "Indicativo Trapassato remoto",
    "Indicativo Futuro anteriore",
    "Congiuntivo Presente",
    "Congiuntivo Passato",
    "Congiuntivo Trapassato",
    "Congiuntivo Imperfetto",
    "Condizionale Presente",
    "Condizionale Passato",
]

# create database if need be
try:
    os.makedirs(HTMLDATA)
    os.makedirs(CSVDATA)
except FileExistsError:
    pass

# write out the csvs, take care about quoting and encoding
def write_full_csv(output, rows):
    with open(output, encoding='utf-8', mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            w.writerow(row)

def read_appdb():
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()

#    verbs = [row[0] for row in c.execute('SELECT verb FROM appdb ORDER BY freq DESC LIMIT 275')]
    verbs = [row[0] for row in c.execute('SELECT verb FROM appdb')]

    return(verbs)

def write_appdb(conjugations):
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()

    c.executemany('INSERT INTO cards VALUES (?,?,?,?)', conjugations)
    conn.commit()

####################
#
####################

def request_contents(url):
    try:
        contents = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return (None)
    return (contents.read().decode(encoding="utf-8", errors="strict"))


def download_verb_data(verb):
    url = ITALIAN_VERB % verb
    datapath = '%s/%s.html' % (HTMLDATA, verb)

    try:
        with (open(datapath, 'r')) as f:
            contents = f.read()
    except FileNotFoundError:
        contents = None

    if not contents:
        contents = request_contents(url)

    if not contents:
        sys.stderr.write('ERROR: [%s] not found' % (verb))
        return (None)

    with open(datapath, 'w') as f:
        f.write(contents)

    soup = BeautifulSoup(contents, 'html.parser')
    body = soup.html.body

    # check for errors
    unknown = body.find_all('div', attrs={'id': "ch_lblWarning"})
    if len(unknown) > 0:
        sys.stderr.write('ERROR: [%s] is not a real verb' % (verb))
        return (None)
    return (body)

def form_level(mobile_title):
    return('_'.join(mobile_title.split()).upper())

def one_block(body, verb, mobile_title):
    cards = []

    for block in body.find_all('div', attrs={"mobile-title": mobile_title}):
        short_form = form_level(mobile_title)
        forms = [li.text for li in block.find_all('li')]
        # there are three separate patterns to account fo:
        # 1) gender neutral 3rd person, len(forms) == 6
        # 2) gender specific 3rd person, len(forms) == 8
        # 3) composto forms feature avere AND  essere forms, len(forms) == 13
        #    for some reason, reverso treats the 3rd person singular as gender neutral, why?
        if len(forms) == 8:
            # case 2)
            cards = [[verb, id, short_form, form] for id, form in enumerate(forms)]
            pass
        elif len(forms) == 6:
            # case 1)
            cards = [
                [verb, 0, short_form, forms[0]],
                [verb, 1, short_form, forms[1]],
                [verb, 2, short_form, re.sub('lei/lui', 'lui', forms[2])],
                [verb, 3, short_form, re.sub('lei/lui', 'lei', forms[2])],
                [verb, 4, short_form, forms[3]],
                [verb, 5, short_form, forms[4]],
                [verb, 6, short_form, re.sub('loro', 'loro(m)', forms[5])],
                [verb, 7, short_form, re.sub('loro', 'loro(f)', forms[5])],
            ]
        elif len(forms) == 13:
            # case 3)
            cards = [
                [verb, 0, short_form, '%s / %s' % (forms[0],                            forms[6])],
                [verb, 1, short_form, '%s / %s' % (forms[1],                            forms[7])],
                [verb, 2, short_form, '%s / %s' % (re.sub('lei/lui', 'lui', forms[2]),  forms[8])],
                [verb, 3, short_form, '%s / %s' % (re.sub('lei/lui', 'lei', forms[2]),  forms[8])],
                [verb, 4, short_form, '%s / %s' % (forms[3],                            forms[9])],
                [verb, 5, short_form, '%s / %s' % (forms[4],                            forms[10])],
                [verb, 6, short_form, '%s / %s' % (re.sub('loro', 'loro(m)', forms[5]), forms[11])],
                [verb, 7, short_form, '%s / %s' % (re.sub('loro', 'loro(f)', forms[5]), forms[12])],
            ]
        return(cards)

def one_verb(verb):
    sys.stderr.write('[%s]\n' % (verb))
    body = download_verb_data(verb)
    if not body:
        sys.stderr.write('error! %s not found' % verb)
        return (None)

    cards = []
    for block in blocks:
        cards += one_block(body, verb, block)

    return (cards)

def main():
    cards = []
    verbs = read_appdb()
    for verb in verbs:
        cards += one_verb(verb)
    write_appdb(cards)

#    write_full_csv(output, cards)

if __name__ == '__main__':
    main()
