from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel)
from random import shuffle, randint

class Question():
    #Содержит вопрос, правильный ответи и три неправильных
    def __init__(self,question,right_answer,wrong1,wrong2,wrong3):
        self.question=question
        self.right_answer = right_answer
        self.wrong1=wrong1
        self.wrong2=wrong2
        self.wrong3=wrong3

questions_list = []
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий'))
questions_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))

app = QApplication([])

#Интерфейс
btn_ok = QPushButton('Ответить') # кнопка ответить
lb_Question = QLabel('В каком году была основана Москва') # Текст вопроса

RadioGroupBox = QGroupBox('Варианты ответов')
rbtn_1 = QRadioButton('1147')
rbtn_2 = QRadioButton('1242')
rbtn_3 = QRadioButton('1861')
rbtn_4 = QRadioButton('1943')

# Все переключатели объединяем в специальную группу. 
#Теперь может быть выбран только один из них.
RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)


layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)


layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # разместили столбцы в одной строке


RadioGroupBox.setLayout(layout_ans1) # готова "панель" с вариантами ответов 

# Создаем панель результата
AnsGroupBox = QGroupBox('Результат теста')
lb_Result = QLabel('прав ты или нет?') # тут будет правильно или нет
lb_Correct = QLabel('Ответ будет тут!') # тут будет текстовка правильного ответа

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter , stretch=2)
AnsGroupBox.setLayout(layout_res)

# Размещение виджетов в окне

layout_line1 = QHBoxLayout() # ВОпрос
layout_line2 = QHBoxLayout() # варианты ответов 
layout_line3 = QHBoxLayout() # кнопка "Ответить"

layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide() # Скрываем панель

layout_line3.addStretch(1)
layout_line3.addWidget(btn_ok,stretch=2) #большая кнопка
layout_line3.addStretch(1)

# теперь строчки делаем друг под другом
layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # пробелы между содержимым

#------------- Старт второй части , функции

def show_result(): # Показываем панель ответов
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_ok.setText('Следующий вопрос')

def show_question(): #Показать панель вопросов
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_ok.setText('Ответить')
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

def ask(q: Question): #Изменённое тело функции со свойствами экземпляра q
#функция записывает значения вопроса и ответов в соответствующие виджеты, при этом варианты ответов распределяются случайным образом
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question)
    lb_Correct.setText(q.right_answer) 
    show_question() 


def show_correct(res):
    ''' показать результат - установим переданный 
    текст в надпись "результат" и покажем нужную панель '''
    lb_Result.setText(res)
    show_result()



def check_answer():
    ''' если выбран какой-то вариант ответа, то надо проверить и показать панель ответов'''
    if answers[0].isChecked():
        show_correct('Правильно!')
        window.score += 1
        print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Неверно!')
            print('Рейтинг: ', (window.score/window.total*100), '%')

#6-ая часть
#задает вопрос из списка
# этой функции нужна переменная, в которой будет указываться номер текущего вопроса
# эту переменную можно сделать глобальной, либо же сделать свойством "глобального объекта" (app или window)
# мы заведем (ниже) свойство window.cur_question.
def next_quextion():
    window.total +=1
    print('Статистика\n - Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
    cur_question = randint(0,len(questions_list)-1)
    q = questions_list[cur_question] #взяли вопрос
    ask(q) #спросили этот вопрос
def click_OK():
    ''' определяет, надо ли показывать другой вопрос либо проверить ответ на этот '''
    if btn_ok.text() == 'Ответить':
        check_answer() #функция проверки ответа
    else:
        next_quextion() #функция след вопроса



window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memory Card')
# текущий вопрос из списка сделаем свойством объекта "окно", так мы сможем спокойно менять его из функции:
btn_ok.clicked.connect(click_OK) # проверяем, что панель ответов показывается при нажатии на кнопку
# все настроено, осталось задать вопрос и показать окно:
window.score = 0
window.total = 0
next_quextion()
window.resize(400,300)
window.show()
app.exec()