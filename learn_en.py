from random import randint
from sqlite3 import connect
from threading import Thread
from tkinter import *

from pyttsx3 import init as tts_init

# Глобавльные переменные
CON = connect('dict.sqlite3')
CUR = CON.cursor()
MAX = CUR.execute('SELECT COUNT(*) FROM Words').fetchone()[0]
LAST = []
LEN = 30


# Озвучить слово
def say(text):
    # tts = tts_init()
    # tts.say(text)
    # tts.runAndWait()

    def _say(text):
        tts = tts_init()
        tts.say(text)

        try:
            tts.runAndWait()
        except RuntimeError:
            # Попытка запустить озвучку до завершения предыдущей
            print('Новая озвучка началась до завершения предыдущей!')

    x = Thread(target=_say, args=(text, ), daemon=True)
    x.start()


# Сгенерировать следующее слово
def next_word():
    global CUR, LAST

    for _ in range(10):
        i = randint(0, MAX)

        if i not in LAST:
            LAST.append(i)

            if len(LAST) > LEN:
                del(LAST[0:-LEN])

            sql = 'SELECT word, vocal, trans FROM Words WHERE id = ?'
            word = CUR.execute(sql, (i, )).fetchone()

            break
    else:
        word = ('Error', '[ˈerər]', 'ошибка!')

    text_word.configure(text=word[0])
    text_vocal.configure(text=word[1])
    text_trans.configure(text=word[2])

    if word is not None:
        say(word[0][:50])


# Общие параметры
window = Tk()
window.title('Словарь английского 3000 слов')
window.geometry('400x150')

# Слово на английском
text_word = Label(window, text='Start', font=('Arial Bold', 24))
text_word.pack()

# Транскрипция
text_vocal = Label(window, text='[stɑːt]', font=('Arial', 12))
text_vocal.pack()

# Перевод
text_trans = Label(window, text='начать', font=('Arial', 14))
text_trans.pack()

# Показать следущее слово
btn = Button(window, text='Далее', command=next_word)
btn.pack()

window.mainloop()

CUR.close()
CON.close()
