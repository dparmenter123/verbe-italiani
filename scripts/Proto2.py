from statemachine import StateMachine, State
import queue

deck = [
    ('section 1', 'card 1'),
    ('section 1', 'card 2'),
    ('section 2', 'card 3'),
    ('section 3', 'card 4'),
    ('section 4', 'card 5'),
    ('section 4', 'card 6'),
    ('section 4', 'card 7'),
]

class AppStateMachine(StateMachine):
    initialize = State('initialize', initial=True)
    build = State('build')
    done = State('done')
    homeview = State('home view')
    settingsview = State('settings view')
    any_to_study_p = State('any to study?')
    sectionview = State('section view')
    frontview = State('front view')
    backview = State('back view')
    correct = State('correct')
    wrong = State('wrong')
    more_todo_p = State('more todo?')
    any_to_redo_p = State('any to redo?')
    new_section_p = State('new section?')
    
    initialize_to_build = initialize.to(build)

    build_to_home_view = build.to(homeview)

    homeview_to_settings = homeview.to(settingsview)
    homeview_to_any_to_study = homeview.to(any_to_study_p)

    settings_to_build = settingsview.to(build)

    any_to_study_yes = any_to_study_p.to(sectionview)
    any_to_study_no = any_to_study_p.to(done)

    sectionview_to_homeview = sectionview.to(homeview)
    sectionview_to_frontview = sectionview.to(frontview)

    frontview_to_homeview = frontview.to(homeview)
    frontview_to_backview = frontview.to(backview)

    backview_to_frontview = backview.to(frontview)
    backview_to_homeview = backview.to(homeview)
    backview_to_wrong = backview.to(wrong)
    backview_to_correct = backview.to(correct)

    correct_to_more_todo = correct.to(more_todo_p)
    wrong_to_more_todo = wrong.to(more_todo_p)

    more_todo_yes = more_todo_p.to(new_section_p)
    more_todo_no = more_todo_p.to(any_to_redo_p)

    any_to_redo_yes = any_to_redo_p.to(new_section_p)
    any_to_redo_no = any_to_redo_p.to(done)

    def on_enter_done(self):
        print('done')

    def on_enter_initialize(self):
        print('initialize', initial=True)

    def on_enter_build(self):
        print('build')

    def on_enter_homeview(self):
        print('home view')

    def on_enter_settingsview(self):
        print('settings view')

    def on_enter_any_to_study_p(self):
        print('any to study?')

    def on_enter_sectionview(self):
        print('section view')

    def on_enter_frontview(self):
        print('front view')

    def on_enter_backview(self):
        print('back view')

    def on_enter_correct(self):
        print('correct')

    def on_enter_wrong(self):
        print('wrong')

    def on_enter_more_todo_p(self):
        print('more todo?')

    def on_enter_any_to_redo_p(self):
        print('any to redo?')

    def on_enter_new_section_p(self):
        print('new section?')

    def __init__(self):
        super(AppStateMachine, self).__init__(self)
        self.todo = queue.SimpleQueue()
        self.redo = queue.LifoQueue()
        self.sections = []
        for section, card in deck:
            if section not in self.sections: self.sections += [section]
            self.todo.put((section, card))
        self.current_card = self.todo.get()

    # done = State('done')
    # initialize = State('initialize', initial=True)
    # build = State('build')
    # homeview = State('home view')
    # settingsview = State('settings view')
    # any_to_study_p = State('any to study?')
    # sectionview = State('section view')
    # frontview = State('front view')
    # backview = State('back view')
    # correct = State('correct')
    # wrong = State('wrong')
    # more_todo_p = State('more todo?')
    # any_to_redo_p = State('any to redo?')
    # new_section_p = State('new section?')

    # def on_enter_home(self):
    #     prompt = '''
    #     +----------------
    #     | HOME:
    #     |
    #     | DUE: {todo} / {redo}
    #     |
    #     | menu:
    #     |  * start
    #     +-----------------
    #     '''
    #     print(prompt.format(todo=self.todo.qsize() + 1,
    #                         redo=self.redo.qsize()))
    #
    # def on_enter_section(self):
    #     prompt = '''
    #     +----------------
    #     | SECTION:
    #     |
    #     |    {section}
    #     |
    #     | menu:
    #     |  * forward
    #     |  * back
    #     +-----------------
    #     '''
    #     print(prompt.format(section=self.current_card[0]))
    #
    # def on_enter_front(self):
    #     prompt = '''
    #     +----------------
    #     | FRONT:
    #     |
    #     |    {card}
    #     |
    #     | menu:
    #     |  * flip
    #     +-----------------
    #     '''
    #     print(prompt.format(card=self.current_card[1]))
    #
    # def on_enter_back(self):
    #     prompt = '''
    #     +----------------
    #     | BACK:
    #     |
    #     |    {card}
    #     |
    #     | menu:
    #     |  * wrong
    #     |  * right_3
    #     |  * right_4
    #     |  * right_5
    #     +-----------------
    #     '''
    #     print(prompt.format(card=self.current_card[1]))
    #
    # def on_enter_wrong(self):
    #     print('wrong')

def main():
    app = AppStateMachine()

if __name__ == '__main__':
    main()
