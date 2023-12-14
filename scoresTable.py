import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
import datetime
import sqlite3 as sql

def showScores():
    win = tk.Tk()
    win.title("Scores")
    win.geometry('600x600')
    # conn = sql.connect('bestScore.db')
    # cu = conn.cursor()
    # cu.execute("SELECT * FROM bestScore")
    # df = pd.read_sql_query("SELECT * FROM bestScore", conn)
    df = pd.read_csv('bestScore.csv')

    table = ttk.Treeview(win, columns=df.columns, height=300)
    table.heading('#1', text=df.columns[0])
    table.heading('#2', text=df.columns[1])
    table.heading('#3', text=df.columns[2])
    #
    table.column('#1', width=200, stretch=False)
    table.column('#2', width=200, stretch=False)
    table.column('#3', width=200, stretch=False)

    for index, row in df.iterrows():
        values = row.tolist()
        table.insert('', 'end', values=values)

    table.pack()
    win.mainloop()

def askSaveScore(score):
    askIf = messagebox.askyesno('Save score', 'Do you want to save your score?')
    if askIf:
        saveScoreWindow(score)
def saveScoreWindow(score):
    winSave = tk.Tk()
    winSave.title('Save score')
    winSave.geometry('200x200')
    name = tk.Entry(winSave)
    label = tk.Label(winSave,text='Enter your name')
    label.pack()
    name.bind('<Return>', lambda event: saveScore(name.get(), score, winSave))
    name.pack()
    winSave.mainloop()
def saveScore(name, score, previousWindow):
    previousWindow.destroy()
    df = pd.read_csv('bestScore.csv')
    new_data = pd.DataFrame({'name': [name],
                             'score': [score],
                             'date': [datetime.date.today().strftime("%d/%m/%Y")]})
    # df =
    df.add(new_data)
    # df.append(new_data, ignore_index=True)
    df.sort_values(by=['score'], inplace=True, ascending=False)
    df.to_csv('bestScore.csv', index=False)
    showScores()

def run():
    showScores()
