import tkinter as tk
import tkinter.ttk as ttk

import field


def startGame(prevWin, fieldSize):
    try:
        prevWin.destroy()
        qwe = field.Field(int(fieldSize[0]))
        qwe.run()
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        while True:
            pass


def helpBox():
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
    win = tk.Tk()
    win.title("2048")
    x = win.winfo_screenwidth()
    y = win.winfo_screenheight()
    win.geometry(f'+{x // 2 -100}+{y // 2-100 }')
    values = ['3x3', '4x4', '5x5', '6x6', '8x8']
    choice = ttk.Combobox(win, values=values)
    greetings = tk.Label(win, text="Hello, this is the copy\nof wellknown game 2048", font="Arial 15")
    c = tk.Label(win, text="Choose field size\nand start playing\n(try to beat best score)", font="Arial 15")
    forHelp = tk.Label(win, text="F1 - help", font="Arial 10 italic")
    credits = tk.Label(win, text="mbugzy", font="Arial 7 italic")
    greetings.pack()
    c.pack()
    choice.pack()
    forHelp.pack()
    credits.pack()
    choice.bind("<<ComboboxSelected>>", lambda event: startGame(win, choice.get()))
    win.bind("<F1>", lambda event: helpBox())
    win.mainloop()
