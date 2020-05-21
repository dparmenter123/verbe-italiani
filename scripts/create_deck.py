import sqlite3
import random
import sys

def genderizer(pos):
    if pos == 2: return(random.choice([2, 3]))
    if pos == 6: return(random.choice([6, 7]))
    return(pos)

def pick_pos(k):
    options = [0,1,2,4,5,6]
    choices = random.sample(options, k=k)
    return([str(genderizer(choice)) for choice in choices])

def one_form(c, verbs, form, k, start, end, level):
    sys.stderr.write('%s:%s\n' % (form, level))
    QUERY = '''
      select c.ROWID, '{level2}', 0, 2.5, 1, 0 from cards c 
      WHERE verb = '{verb}' 
      AND c.form ='{form}'
      AND pos IN ({pos})
      '''
    cards = []
    for verb in verbs[start:end]:
        pos = pick_pos(k)
        q = QUERY.format(verb=verb, form=form, pos=','.join(pos), level2=level)
        print(q)
        for row in c.execute(q):
            cards += [row]
    return(cards)

def main():
    conn = sqlite3.connect('/Users/davidp/work/verbe-italiani/data/db/app.db')
    c = conn.cursor()

    # all the verbs, ordered
    QUERY = '''
      select a.verb from appdb a
      ORDER BY a.freq DESC
      LIMIT 75
    '''
    verbs = [row[0] for row in c.execute(QUERY)]
    c = conn.cursor()

    cards = []
    cards += one_form(c, verbs, 'INDICATIVO_PASSATO_PROSSIMO', 3, 0, 50, "A1")
    cards += one_form(c, verbs, 'INDICATIVO_PASSATO_PROSSIMO', 1, 51, 250, "A2")
    # cards += one_form(c, verbs, 'INDICATIVO_PASSATO_PROSSIMO', 1, 251, 500, "B1")
    # cards += one_form(c, verbs, 'INDICATIVO_PASSATO_PROSSIMO', 1, 501, 1000, "B2")

    # cards += one_form(c, verbs, 'INDICATIVO_FUTURO_SEMPLICE', 1, 0, 250, "A2")
    # cards += one_form(c, verbs, 'INDICATIVO_FUTURO_SEMPLICE', 1, 251, 500, "B1")
    # cards += one_form(c, verbs, 'INDICATIVO_FUTURO_SEMPLICE', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'INDICATIVO_IMPERFETTO', 1, 0, 250, "A2")
    # cards += one_form(c, verbs, 'INDICATIVO_IMPERFETTO', 1, 251, 500, "B1")
    # cards += one_form(c, verbs, 'INDICATIVO_IMPERFETTO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONDIZIONALE_PRESENTE', 1, 0, 250, "A2")
    # cards += one_form(c, verbs, 'CONDIZIONALE_PRESENTE', 1, 251, 500, "B1")
    # cards += one_form(c, verbs, 'CONDIZIONALE_PRESENTE', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONGIUNTIVO_PRESENTE', 1, 0, 250, "A2")
    # cards += one_form(c, verbs, 'CONGIUNTIVO_PRESENTE', 1, 251, 500, "B1")
    # cards += one_form(c, verbs, 'CONGIUNTIVO_PRESENTE', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'INDICATIVO_TRAPASSATO_PROSSIMO', 1, 0, 500, "B1")
    # cards += one_form(c, verbs, 'INDICATIVO_TRAPASSATO_PROSSIMO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONGIUNTIVO_IMPERFETTO', 1, 0, 500, "B1")
    # cards += one_form(c, verbs, 'CONGIUNTIVO_IMPERFETTO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONGIUNTIVO_PASSATO', 1, 0, 500, "B1")
    # cards += one_form(c, verbs, 'CONGIUNTIVO_PASSATO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONGIUNTIVO_TRAPASSATO', 1, 0, 500, "B1")
    # cards += one_form(c, verbs, 'CONGIUNTIVO_TRAPASSATO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'CONDIZIONALE_PASSATO', 1, 0, 500, "B1")
    # cards += one_form(c, verbs, 'CONDIZIONALE_PASSATO', 1, 501, 1000, "B2")
    #
    # cards += one_form(c, verbs, 'INDICATIVO_PASSATO_REMOTO', 1, 0, 1000, "B2")
    # cards += one_form(c, verbs, 'INDICATIVO_TRAPASSATO_REMOTO', 1, 0, 1000, "B2")
    # cards += one_form(c, verbs, 'INDICATIVO_FUTURO_ANTERIORE', 1, 0, 1000, "B2")
    c.executemany('INSERT INTO carddeck VALUES (?,?,?,?,?,?)', cards)
    conn.commit()

if __name__ == '__main__':
    main()