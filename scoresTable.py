import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import pandas as pd

def getBest(fieldSize):
    df = pd.read_csv('bestScore.csv')
    a = df[df['field'] == fieldSize]
    return a['score'].max()

def showScores(fieldSize):
    win = tk.Tk()
    win.title("Scores")
    win.geometry('300x400')
    win.resizable(False, False)

    df = pd.read_csv('bestScore.csv')

    table = ttk.Treeview(win, columns=df.columns, height=300)
    table.heading('#1', text='place')
    table.heading('#2', text=df.columns[1])
    table.heading('#3', text=df.columns[2])
    table.heading('#4', text=df.columns[3])
    #
    table.column('#0', width=0, stretch=False)
    table.column('#1', width=50, stretch=False)
    table.column('#2', width=80, stretch=False)
    table.column('#3', width=100, stretch=False)
    table.column('#4', width=70, stretch=False)

    i = 1
    for index, row in df.iterrows():
        values = row.tolist()
        if values[0] == fieldSize:
            table.insert('', 'end', values=[i] + values[1:])
            i += 1
        if i == 10:
            break

    table.pack()
    win.mainloop()


def askSaveScore(score, fieldSize):
    winAsk = tk.Tk()
    winAsk.title('Save score')
    winAsk.geometry('200x50')
    winAsk.resizable(False, False)
    ttk.Label(winAsk, text='Do you want to save your score?').pack()
    ttk.Button(winAsk, text='Yes', command=lambda: saveScoreWindow(score, fieldSize, winAsk)).pack()
    winAsk.mainloop()



def saveScoreWindow(score, fieldSize,previousWindow=None):
    if previousWindow:
        previousWindow.destroy()
    winSave = tk.Tk()
    winSave.title('Save score')
    name = tk.Entry(winSave)
    label = tk.Label(winSave, text='Enter your name')
    label.pack()
    name.bind('<Return>', lambda event: saveScore(name.get(), score, fieldSize, winSave))
    name.pack()
    tk.Button(winSave, text='Save score', command=lambda: saveScore(name.get(), score, fieldSize, winSave)).pack()
    x = winSave.winfo_screenwidth()
    y = winSave.winfo_screenheight()
    winSave.geometry(f'300x100+{x // 2 - 150}+{y // 2 - 50}')
    winSave.mainloop()


def saveScore(name, score, fieldSize, previousWindow):
    previousWindow.destroy()
    df = pd.read_csv('bestScore.csv')

    df.loc[len(df.index)] = [fieldSize, score, name, datetime.date.today().strftime('%d/%m/%Y')]
    df.sort_values(by=['score'], inplace=True, ascending=False)
    df.to_csv('bestScore.csv', index=False)
    showScores(fieldSize)
