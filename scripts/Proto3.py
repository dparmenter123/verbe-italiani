import enum
import queue
from transitions import Machine

TODAY = 0

class Card:
    def __init__(self, section, id, repetitions=0, interval=1, easiness=2.5, next_practice=0):
        self.section = section
        self.id = id
        self.repetitions = repetitions
        self.interval = interval
        self.easiness = easiness
        self.next_practice = next_practice


CARD_DECK = [
    Card('section 1', 1),
    Card('section 1', 2),
    Card('section 2', 3),
    Card('section 3', 4),
    Card('section 4', 5),
    Card('section 4', 6),
    Card('section 4', 7),
]


class Proto3Model(object):
    def __init__(self, cursor, level):
        self.cursor = cursor
        self.level = level
        self.todo = queue.SimpleQueue()
        self.redo = queue.SimpleQueue()
        self.card = None

    def on_enter_BUILD(self):
        print('building!')
        self.homeview()

    def on_enter_HOME_VIEW(self):
        print('homeview...')

    def on_enter_ANY_TO_STUDY(self):
        print('any to study?')
        if 0:
            self.any_to_study_no()
        else:
            self.any_to_study_yes()

    def on_enter_DONE(self):
        print('done!')

    def on_enter_SECTION_VIEW(self):
        print('Section view!')

    def on_enter_FRONT_VIEW(self):
        print('Front view!')

    def on_enter_BACK_VIEW(self):
        print('Back view!')

    def on_enter_WRONG(self):
        print('WRONG!')

    def on_enter_CORRECT(self):
        print('CORRECT!')

# The states
class States(enum.Enum):
    ERROR = 0
    START = 1
    BUILD = 2
    HOME_VIEW = 3
    ANY_TO_STUDY = 4
    SECTION_VIEW = 5
    FRONT_VIEW = 6
    BACK_VIEW = 7
    CORRECT = 8
    WRONG = 9
    MORE_TODO = 10
    ANY_TO_REDO = 11
    NEW_SECTION = 12
    DONE = 99

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    ['build', States.START, States.BUILD ],
    ['homeview', States.BUILD, States.HOME_VIEW ],
    ['study', States.HOME_VIEW, States.ANY_TO_STUDY ],
    ['any_to_study_no', States.ANY_TO_STUDY, States.DONE ],
    ['any_to_study_yes', States.ANY_TO_STUDY, States.SECTION_VIEW ],
    ['front', States.SECTION_VIEW, States.FRONT_VIEW ],
    ['flip', States.FRONT_VIEW, States.BACK_VIEW ],
    ['flip_back', States.BACK_VIEW, States.FRONT_VIEW ],
    ['home1', States.SECTION_VIEW, States.HOME_VIEW],
    ['home2', States.FRONT_VIEW, States.HOME_VIEW],
    ['wrong', States.BACK_VIEW, States.WRONG],
    ['correct', States.BACK_VIEW, States.CORRECT],
    ['correct2', States.CORRECT, States.MORE_TODO],
    ['wrong2', States.WRONG, States.MORE_TODO],
    ['more_to_do_yes', States.MORE_TODO, States.NEW_SECTION],
    ['more_to_do_no', States.MORE_TODO, States.ANY_TO_REDO],
    ['any_to_redo_yes', States.ANY_TO_REDO, States.NEW_SECTION],
    ['any_to_redo_no', States.ANY_TO_REDO, States.DONE],
    ['new_section_yes', States.NEW_SECTION, States.SECTION_VIEW],
    ['new_section_no', States.NEW_SECTION, States.FRONT_VIEW]
]


model = Proto3Model('cursor', 'A1')
machine = Machine(model, states=States, transitions=transitions, initial=States.START)
print(model.state)
model.build()
model.study()
model.front()
model.flip()
model.flip_back()
model.flip()
model.correct()
