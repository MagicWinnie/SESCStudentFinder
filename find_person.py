import os
import ctypes
import pickle
import rawpy
import numpy as np
import pandas as pd

from typing import *
import Levenshtein
import face_recognition

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image

app = tk.Tk()

# theme
app.tk.call('source', 'azure-theme/azure-dark.tcl')
ttk.Style().theme_use('azure-dark')

app.title("DeAnonSESC")
app.geometry('1280x640')

tabControl = ttk.Notebook(app)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text = 'Поиск фото по имени')
tabControl.add(tab2, text = 'Поиск информации по фото')
tabControl.pack(expand = 1, fill = "both")

def is_ru_lang_keyboard():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'

def keys(event):
    if is_ru_lang_keyboard():
        if event.keycode==86:
            event.widget.event_generate("<<Paste>>")
        if event.keycode==67: 
            event.widget.event_generate("<<Copy>>")    
        if event.keycode==88: 
            event.widget.event_generate("<<Cut>>")    
        if event.keycode==65535: 
            event.widget.event_generate("<<Clear>>")
        if event.keycode==65: 
            event.widget.event_generate("<<SelectAll>>")

# ====TAB 1====
def search_tab_1(name: str):
    m = 0
    data = None

    for f in os.listdir('csv_classes'):
        df = pd.read_csv(os.path.join('csv_classes', f), encoding='utf-16')

        for i in df.itertuples():
            jaro = Levenshtein.jaro(i._1, name)
            if jaro > m:
                m = jaro
                data = i
    
    return data if m >= 0.5 else None

def clicked_tab_1():
    global image_tab_1, txt_tab_1, tab1

    name = txt_tab_1.get()

    data = search_tab_1(name)
    if data is not None:
        messagebox.showinfo(
            'Ученик найден',
            '\n'.join(
                [
                    'Имя: {}'.format(data._1),
                    'Группа: {:03d}'.format(int(data.Группа))
                ]
            )
        )
        
        temp_image = ImageTk.PhotoImage(Image.open(data._5))
        image_tab_1.configure(image=temp_image)
        image_tab_1.image = temp_image
    else:
        messagebox.showinfo(
            'Ученик не найден',
            'Попробуйте уточнить запрос...'
        )

        image_tab_1.configure(image=empty_image)
        image_tab_1.image = empty_image

ttk.Label(
    tab1, 
    text = "Поиск фото ученика СУНЦ НГУ по имени.\nПоиск ведется по базе данных электронного журнала СУНЦ НГУ.\nРазрешение изображений: 125x125.\nЭто может занять некоторое время.",
    font = ("Arial", 16)
).grid(
    column = 0, 
    row = 0,
    padx = 30,
    pady = 30
)  

txt_tab_1 = ttk.Entry(
    tab1,
    width = 75
)
txt_tab_1.grid(
    column = 0,
    row = 1,
    padx = 30,
    sticky = "W"
)
txt_tab_1.bind("<Control-KeyPress>", keys)

ttk.Button(
    tab1,
    text = "Поиск",
    command = clicked_tab_1
).grid(
    column = 0,
    row = 2,
    padx = 30,
    pady = 30,
    sticky = "W"
)

ttk.Label(
    tab1,
    text = "Изображение:",
    font = ("Arial", 14)
).grid(
    column = 0,
    row = 3,
    padx = 30,
    pady = 30
)

empty_image = ImageTk.PhotoImage(Image.open("empty.png"))
image_tab_1 = ttk.Label(tab1, image = empty_image)
image_tab_1.grid(
    column = 0,
    row = 4,
    columnspan = 2
)


# ====TAB 2====
with open('dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))

def open_file():
    global image_tab_2_1, image_tab_2_2, tab2

    file_path = askopenfile(mode='r', filetypes=[('Image Files', '.jpeg .jpg .png .CR2 .tiff')])
    
    path = file_path.name
    
    if file_path is not None:
        if path.lower().endswith('cr2'):
            img = rawpy.imread(path).postprocess()
        else:
            img = Image.open(path)
            img = img.convert('RGB')
            img = np.array(img)
        try:
            data = mapper(search_tab_2(img, known_face_names, known_face_encodings)[0])
        except Exception as e:
            messagebox.showinfo(
                'Ученик не найден или не распознано лицо.',
                'Попробуйте загрузить другую фотографию или убедитесь, что данный ученик обучается в СУНЦ НГУ...\nОшибка: {}'.format(e)
            )
            image_tab_2_1.configure(image=empty_image)
            image_tab_2_1.image = empty_image

            image_tab_2_2.configure(image=empty_image)
            image_tab_2_2.image = empty_image
        else:
            if data is not None:
                tmp_img = Image.fromarray(img)
                tmp_img.thumbnail((200, 200), Image.ANTIALIAS)
                temp_image = ImageTk.PhotoImage(tmp_img)
                image_tab_2_1.configure(image=temp_image)
                image_tab_2_1.image = temp_image

                temp_image_2 = ImageTk.PhotoImage(Image.open(data._5))
                image_tab_2_2.configure(image=temp_image_2)
                image_tab_2_2.image = temp_image_2

                messagebox.showinfo(
                    'Ученик найден',
                    '\n'.join(
                        [
                            'Имя: {}'.format(data._1),
                            'Группа: {:03d}'.format(int(data.Группа))
                        ]
                    )
                )
            else:
                messagebox.showinfo(
                    'Ученик не найден или не распознано лицо.',
                    'Попробуйте загрузить другую фотографию или убедитесь, что данный ученик обучается в СУНЦ НГУ...'
                )
                image_tab_2_1.configure(image=empty_image)
                image_tab_2_1.image = empty_image

                image_tab_2_2.configure(image=empty_image)
                image_tab_2_2.image = empty_image
    else:
        messagebox.showinfo(
            'Путь к файлу недействителен',
            'Попробуйте повторить...'
        )
        image_tab_2_1.configure(image=empty_image)
        image_tab_2_1.image = empty_image

        image_tab_2_2.configure(image=empty_image)
        image_tab_2_2.image = empty_image

        '''
        temp_image = ImageTk.PhotoImage(Image.open(data._5))
        image_tab_1.configure(image=temp_image)
        image_tab_1.image = temp_image
        '''

def search_tab_2(img: np.ndarray, known_face_names: List, known_face_encodings: np.ndarray) -> List:
    '''
    img: rgb image
    '''
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = None

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_names

def mapper(name: str):
    for f in os.listdir('csv_classes'):
        df = pd.read_csv(os.path.join('csv_classes', f), encoding='utf-16')
        
        for i in df.itertuples():
            if '_'.join(i._5.replace('\\', '/').split('/')[-2:]) == name:
                return i

ttk.Label(
    tab2,
    text = "Поиск имени, класса и номера группы по фотографии ученика СУНЦ НГУ.\nВнимание! Возможно ошибочное определение. Это может занять несколько минут.",
    font = ("Arial", 16)
).grid(
    column = 0,
    row = 0, 
    padx = 30,
    pady = 30
)

user_image_btn = ttk.Button(
    tab2, 
    text = 'Выберите файл', 
    command = lambda: open_file()
)
user_image_btn.grid(
    column = 0,
    row = 1,
    padx = 30,
    sticky = "W"
)

ttk.Label(
    tab2,
    text = "Изображения:",
    font = ("Arial", 14)
).grid(
    column = 0,
    row = 2,
    padx = 30,
    pady = 30,
    columnspan=2
)

image_tab_2_1 = ttk.Label(tab2, image = empty_image)
image_tab_2_1.grid(
    column = 0,
    row = 3
)
image_tab_2_2 = ttk.Label(tab2, image = empty_image)
image_tab_2_2.grid(
    column = 1,
    row = 3
)

app.mainloop()

