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
HTMLDATA = 'data/html'
CSVDATA = 'data/csvs'

blocks = {
    "Indicativo Presente": "Presente",
    "Indicativo Imperfetto" : "Imperfetto",
    "Indicativo Passato remoto" : "Passato Remoto",
    "Indicativo Futuro semplice" : "Futuro",
    "Indicativo Passato prossimo" : "Perfetto",
    "Indicativo Trapassato prossimo" : "Trapassato Prossimo",
    "Indicativo Futuro anteriore" : "Futuro Anteriore",
    "Congiuntivo Presente" : "Congiuntivo Presente",
    "Congiuntivo Passato" : "Congiuntivo Perfetto",
    "Congiuntivo Trapassato" : "Congiuntivo Trapassato",
    "Congiuntivo Imperfetto" : "Congiuntivo Imperfetto",
    "Condizionale Presente" : "Condizionale Presente",
    "Condizionale Passato" : "Condizionale Passato",
}

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

def one_block(body, verb, mobile_title):
    mood_tense = mobile_title.split(' ')
    mood = mood_tense[0]
    tense = ' '.join(mood_tense[1:])
    for block in body.find_all('div', attrs={"mobile-title": mobile_title}):
        forms = [li.text for li in block.find_all('li')]
        # there are three separate patterns to account fo:
        # 1) gender neutral 3rd person, len(forms) == 6
        # 2) gender specific 3rd person, len(forms) == 8
        # 3) composto forms feature avere AND  essere forms, len(forms) == 13
        #    for some reason, reverso treats the 3rd person singular as gender neutral, why?
        if len(forms) == 8:
            # case 2)
            # all is well, do nothing
            pass
        elif len(forms) == 6:
            # case 1)
            forms = [
                forms[0],
                forms[1],
                re.sub('lei/lui', 'lui', forms[2]),
                re.sub('lei/lui', 'lei', forms[2]),
                forms[3],
                forms[4],
                re.sub('loro', 'loro(m)', forms[5]),
                re.sub('loro', 'loro(f)', forms[5]),
            ]
        elif len(forms) == 13:
            # case 2)
            forms = [
                '%s / %s' % (forms[0],                            forms[6]),
                '%s / %s' % (forms[1],                            forms[7]),
                '%s / %s' % (re.sub('lei/lui', 'lui', forms[2]),  forms[8]),
                '%s / %s' % (re.sub('lei/lui', 'lei', forms[2]),  forms[8]),
                '%s / %s' % (forms[3],                            forms[9]),
                '%s / %s' % (forms[4],                            forms[10]),
                '%s / %s' % (re.sub('loro', 'loro(m)', forms[5]), forms[11]),
                '%s / %s' % (re.sub('loro', 'loro(f)', forms[5]), forms[12]),
            ]
        return ({mobile_title : forms})

def one_verb(pos, verb):
    sys.stderr.write('[%s]\n' % (verb))
    body = download_verb_data(verb)
    if not body:
        return (None)

    present = one_block(body, verb, "Indicativo Presente")["Indicativo Presente"]

    forms = {}
    for block in blocks.keys():
        forms.update(one_block(body, verb, block))

    cards = []
    for block in blocks.keys():
        # print out all the forms
        for i in range(8):
            front = '%s -> %s' % (present[i], blocks[block])
            back = forms[block][i]
            cards += [[pos, i, verb, blocks[block], front, back]]
    return (cards)


def main(path, output):
    cards = [['Position', 'POS', 'Verb', 'Form', 'Front', 'Back']]
    with open(path) as f:
        for pos, verb in enumerate(f.readlines()):
            if (verb[0] == '#'):
                # strip out comments
                pass
            else:
                cards += one_verb(pos, verb.strip())

    write_full_csv(output, cards)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
