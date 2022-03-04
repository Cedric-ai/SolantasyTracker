from tkinter import *
from tkinter import ttk
import DataGraber
from DataGraber import create_graph
from functools import partial
from tkinter.ttk import Progressbar
from tkinter import filedialog as fd

import sys, os

os.chdir(sys._MEIPASS)
width = 30
filename = ""

def main():


    def get_data(search_req):
        p = Progressbar(root, orient=HORIZONTAL, length=200, mode="determinate", takefocus=True, maximum=6)
        p.pack()
        root.update()
        create_graph(search_req, p, root, filename)
        p.destroy()
        root.update()

    def select_chrome():
        global filename
        filename = fd.askopenfilename()

    root = Tk()
    root.title("Solantasy NFT Tracker")

    solwarriors = Button(root, text="SolWarriors", command=partial(get_data, "solwarriors"), width=width)
    solwarriors.pack()
    solwizards = Button(root, text="SolWizards", command=partial(get_data, "solwizards"), width=width)
    solwizards.pack()
    solarchers = Button(root, text="SolArchers", command=partial(get_data, "solarchers"), width=width)
    solarchers.pack()

    choose_driver = Button(root, text="Select your ChromeDriver", command=select_chrome, width=width)
    choose_driver.pack()

    T = Text(root, height=2, width=width)
    T.pack()
    T.insert(END, "Donate $SOL: HSnpiFgASRi69Jxm8PYCwKTczn7tfzpZRfmcs3gvPhh2")



    root.mainloop()


if __name__ == '__main__':
    main()
