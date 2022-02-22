import tkinter
from run import run


def open():
    run()


app = tkinter.Tk()
app.title("Napoleon Defense")
app.geometry("1625x975")

lb = tkinter.Label(app, text="Start game").pack()
bt = tkinter.Button(app, text="Tkinter", command=open()).pack()

app.mainloop()
