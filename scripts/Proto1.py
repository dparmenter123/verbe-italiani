import sqlite3
import cmd
import queue

from forms import MATCHING_FORMS

###########################
#
###########################

class AppSettings:
    def __init__(self, level):
        self.level = level
        self.db = '/Users/davidp/work/verbe-italiani/data/db/app.db'


class OneCard:
    def __init__(self):
        pass

    def load(self, cursor, id):
        rows = [row for row in cursor.execute('select form, verb, pos, conjugation from cards WHERE ROWID = {ID}'.format(ID=id))]

        self.cardid = id
        self.form, self.verb, self.pos, self.conjugation = rows[0]
        return(self)

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

    def card_back(self, cursor, level):
        CARD_BACK = '''
        +------------------------------------+
        |
        |    ({form1})
        |    
        |    {conjugation1}
        |    ---------------------
        |    ({form2})
        |    
        |    {conjugation2}
        |    
        +------------------------------------+
        '''
        form1, conjugation, form2, _ = self.generate_prompt(cursor, level)
        return (
            CARD_BACK.format(level=level, form1=form1.lower(),
                              conjugation1=conjugation.upper(), form2=form2.lower(), conjugation2=self.conjugation)
        )

def StudySession:
    def __init__(self, cards):
        self.review = queue.SimpleQueue()
        self.redo = set()

class Proto1App(cmd.Cmd):
    def __init__(self, cursor, level):
        super(Proto1App, self).__init__()
        self.cursor = cursor
        self.level = level
        self.card = 1001

    def do_front(self, line):
        card = OneCard().load(self.cursor, self.card)
        print(card.card_front(self.cursor, self.level))

    def do_back(self, line):
        card = OneCard().load(self.cursor, self.card)
        print(card.card_back(self.cursor, self.level))

    def do_5(self, line):
        self.card += 1
        self.do_front(line)

    def emptyline(self, line):
        pass


    def do_EOF(self, line):
        return True


def main():
    SETTINGS = AppSettings("B1")

    conn = sqlite3.connect(SETTINGS.db)
    cursor = conn.cursor()

    app = Proto1App(cursor, SETTINGS.level)
    app.cmdloop()

    # card = OneCard().load(c, 1000)
    # print(card.card_front(c, SETTINGS.level))
    # print(card.card_back(c, SETTINGS.level))



if __name__ == '__main__':
    main()
