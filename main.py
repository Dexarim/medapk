import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class QuestionnaireApp(App):
    def build(self):
        self.bruise = 0
        self.sprain = 0
        self.fracture = 0
        self.dislocation = 0
        self.chronic_disease = 0

        self.questions = [
            {
                'question': "Можно ли двигать конечностью?",
                'answers': [
                    ('да, но с болью', self.process_move_with_pain),
                    ('нет', self.process_cannot_move),
                    ('частично', self.process_partial_movement),
                    ('функции не изменились', self.process_unchanged),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Тип боли:",
                'answers': [
                    ('острая (ярко выраженная)', self.process_acute_pain),
                    ('тупая (неярко выраженная, на большой области)', self.process_dull_pain),
                    ('ноющая боль', self.process_aching_pain),
                    ('только при нагрузках не затрагивает весь сустав', self.process_pain_on_load),
                    ('продолжительная, в течение нескольких месяцев', self.process_long_duration_pain),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Есть синяк или отек?",
                'answers': [
                    ('да', self.process_swelling_or_bruise),
                    ('нет', self.process_no_swelling_or_bruise),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Конечность несет вес при ходьбе?",
                'answers': [
                    ('да', self.process_weight_bearing),
                    ('нет', self.process_non_weight_bearing),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Была травма или удар?",
                'answers': [
                    ('да', self.process_injury_or_blow),
                    ('нет', self.process_no_injury_or_blow),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Есть ограничение движения?",
                'answers': [
                    ('да', self.process_movement_limitation),
                    ('нет', self.process_no_movement_limitation),
                    ('другой ответ', self.process_other_response)
                ]
            },
            {
                'question': "Была предыдущая травма или проблема в этой области?",
                'answers': [
                    ('да', self.process_previous_injury_or_issue),
                    ('нет', self.process_no_previous_injury_or_issue),
                    ('другой ответ', self.process_other_response)
                ]
            },
        ]

        self.current_question_index = 0

        self.layout = BoxLayout(orientation='vertical')
        self.question_label = Label(text=self.questions[0]['question'])
        self.layout.add_widget(self.question_label)

        self.answer_buttons = []
        for answer, callback in self.questions[0]['answers']:
            button = Button(text=answer)
            button.bind(on_press=callback)
            self.answer_buttons.append(button)
            self.layout.add_widget(button)

        return self.layout

    def process_move_with_pain(self, instance):
        self.bruise += 1
        self.fracture += 1
        self.next_question()

    def process_cannot_move(self, instance):
        self.fracture += 1
        self.dislocation += 1
        self.next_question()

    def process_partial_movement(self, instance):
        self.sprain += 1
        self.next_question()

    def process_unchanged(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def process_other_response(self, instance):
        self.next_question()

    def process_acute_pain(self, instance):
        self.dislocation += 1
        self.fracture += 1
        self.next_question()

    def process_dull_pain(self, instance):
        self.bruise += 1
        self.fracture += 1
        self.next_question()

    def process_aching_pain(self, instance):
        self.sprain += 1
        self.fracture += 1
        self.next_question()

    def process_pain_on_load(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def process_long_duration_pain(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def process_swelling_or_bruise(self, instance):
        self.bruise += 1
        self.dislocation += 1
        self.next_question()

    def process_no_swelling_or_bruise(self, instance):
        self.sprain += 1
        self.chronic_disease += 1
        self.next_question()

    def process_weight_bearing(self, instance):
        self.sprain += 1
        self.next_question()

    def process_non_weight_bearing(self, instance):
        self.dislocation += 1
        self.next_question()

    def process_injury_or_blow(self, instance):
        self.sprain += 1
        self.next_question()

    def process_no_injury_or_blow(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def process_movement_limitation(self, instance):
        self.sprain += 1
        self.next_question()

    def process_no_movement_limitation(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def process_previous_injury_or_issue(self, instance):
        self.sprain += 1
        self.next_question()

    def process_no_previous_injury_or_issue(self, instance):
        self.chronic_disease += 1
        self.next_question()

    def next_question(self):
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.question_label.text = self.questions[self.current_question_index]['question']

            for button in self.answer_buttons:
                self.layout.remove_widget(button)

            self.answer_buttons = []
            for answer, callback in self.questions[self.current_question_index]['answers']:
                button = Button(text=answer)
                button.bind(on_press=callback)
                self.answer_buttons.append(button)
                self.layout.add_widget(button)
        else:
            # All questions answered, calculate diagnosis
            diagnosis = self.calculate_scores(self.bruise, self.sprain, self.fracture, self.dislocation, self.chronic_disease)
            self.layout.add_widget(Label(text="Диагноз: " + diagnosis))

    def calculate_scores(self, bruise, sprain, fracture, dislocation, chronic_disease):
        # Perform calculations to determine the diagnosis based on the scores
        # This part will depend on your specific criteria and scoring system
        # Here's a simple example based on the accumulated scores
        scores = {'синяк': bruise, 'вывих': dislocation, 'перелом': fracture, 'растяжение': sprain, 'хроническое заболевание': chronic_disease}
        diagnosis = max(scores, key=scores.get)
        return diagnosis

# Запуск приложения
QuestionnaireApp().run()
