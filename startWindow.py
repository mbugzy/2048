import tkinter as tk
import tkinter.ttk as ttk

import field

choice = None
win = None
def startGame(event):
    global choice, win
    fieldSize = choice.get()
    win.destroy()
    qwe = field.Field(int(fieldSize[0]))
    qwe.run()
    print('last:')
    for row in qwe.matrix:
        for val in row:
            print("{0:>{w}.{p}f}".format(val, w=5, p=0), end=" ")
        print()


def helpBox(event):
    help = tk.Tk()
    help.title("Help")
    helpText = tk.Label(help, text="controls:")
    helpText.pack()
    helpText2 = tk.Label(help,
                         text="right arrow key - move right\nleft arrow key - move left\nup arrow key - move "
                              "up\ndown arrow key - move down\nr - restart\nq - quit\ns - see score")

    helpText2.pack()
    help.mainloop()
    return 'break'

def run():
    global choice, win
    win = tk.Tk()
    win.title("2048")
    values = ['3x3', '4x4', '5x5', '6x6', '8x8']
    choice = ttk.Combobox(win, values=values)
    greatings = tk.Label(win, text="Hello, this is the copy\nof wellknown game 2048", font="Arial 10")
    c = tk.Label(win, text="Choose field size\nand start playing\n(try to beat best score)", bg="black", fg="white",
                 font="Arial 10")
    credits = tk.Label(win, text="mbugzy", font="Arial 5 italic")
    greatings.pack()
    c.pack()
    choice.pack()
    credits.pack()
    choice.bind("<<ComboboxSelected>>", startGame)
    win.bind("<F1>", helpBox)
    win.mainloop()
