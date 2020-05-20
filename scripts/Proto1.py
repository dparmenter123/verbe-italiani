import sqlite3
from forms import MATCHING_FORMS

###########################
#
###########################

class AppSettings:
    def __init__(self, level):
        self.level = level
        self.db = '/Users/davidp/work/verbe-italiani/data/db/app.db'


class OneCard:
    def __init__(self, id, form, verb, pos):
        self.cardid = id
        self.form = form
        self.verb = verb
        self.pos = pos

    def display_pos(self):
        pos_map = {
            0: "io",
            1: "tu",
            2: "lui",
            3: "lei",
            4: "noi",
            5: "voi",
            6: "loro(m)",
            7: "loro(f)",
        }
        if self.form in ['CONGIUNTIVO_PRESENTE', 'CONGIUNTIVO_IMPERFETTO', 'CONGIUNTIVO_PASSATO',
                         'CONGIUNTIVO_TRAPASSATO']:
            prefix = 'che '
        else:
            prefix = ''
        return(prefix + pos_map[self.pos])

    def generate_prompt(self, cursor, level):
        QUERY = '''
           SELECT f.display, c.conjugation FROM cards c INNER JOIN forms f ON c.form = f.form 
           WHERE c.verb = '{verb}' 
                AND pos = {pos} AND c.form IN ({forms}) 
                ORDER BY RANDOM() LIMIT 1
            '''
        forms = ','.join(MATCHING_FORMS[(level, self.form)])
        q = QUERY.format(verb=self.verb, pos=self.pos, forms=forms)
        rows = [row for row in cursor.execute(q)]
        form1, conjugation = rows[0]

        rows = [row for row in cursor.execute("select display from forms where form = '{form}'".format(form = self.form))]
        form2 = rows[0][0]
        return (form1, conjugation, form2, self.display_pos())

    def card_front(self, cursor, level):
        CARD_FRONT = '''
        +------------------------------------+
        |
        |    ({form1})
        |    
        |    {conjugation1}
        |    ---------------------
        |    ({form2})
        |    
        |    {prompt} _________?
        |    
        +------------------------------------+
        '''
        form1, conjugation, form2, prompt = self.generate_prompt(cursor, level)
        return (
            CARD_FRONT.format(level=level, form1=form1.lower(),
                              conjugation1=conjugation.upper(), form2=form2.lower(), prompt=prompt)
        )





###########################
#
###########################

def main():
    SETTINGS = AppSettings("B1")
    card = OneCard(123, "CONGIUNTIVO_PASSATO", 'pensare', 7)

    conn = sqlite3.connect(SETTINGS.db)
    c = conn.cursor()
    print(card.card_front(c, SETTINGS.level))

if __name__ == '__main__':
    main()
