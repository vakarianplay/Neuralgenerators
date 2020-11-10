#!/usr/bin/python
import codecs
import os.path
import tkinter
import tkinter.messagebox
import tkinter.filedialog

#from pip._vendor.appdirs import unicode
from pip._vendor.appdirs import unicode

from logic import *


class GUI():
    input = None
    output = None
    stem = None
    charset = None
    pair = None

    oldInput = ''
    oldStem = -1

    Markov = Markov()

    def __init__(self):
        self.mainWindow = tkinter.Tk()
        self.mainWindow.title("py")

        self.input = tkinter.StringVar()
        self.output = tkinter.StringVar()
        self.words = tkinter.IntVar()
        self.stem = tkinter.IntVar()
        self.charset = tkinter.StringVar()
        self.pair = tkinter.StringVar()

        self.words.set(5000)
        self.stem.set(1)

        inputLabel = tkinter.Label(self.mainWindow, text="Input")
        inputLabel.grid(row=0, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.inputEntry = tkinter.Entry(self.mainWindow, width=25, textvariable=self.input)
        self.inputEntry.grid(row=0, column=1)
        self.inputButton = tkinter.Button(self.mainWindow, text="Choose...", command=self.setInFile)
        self.inputButton.grid(row=0, column=2, sticky=tkinter.E + tkinter.W)

        outputLabel = tkinter.Label(self.mainWindow, text="Output")
        outputLabel.grid(row=1, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.outputEntry = tkinter.Entry(self.mainWindow, width=25, textvariable=self.output)
        self.outputEntry.grid(row=1, column=1)
        self.outputButton = tkinter.Button(self.mainWindow, text="Choose...", command=self.setOutFile)
        self.outputButton.grid(row=1, column=2, sticky=tkinter.E + tkinter.W)

        charsetLabel = tkinter.Label(self.mainWindow, text="Charset")
        charsetLabel.grid(row=2, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.charsetEntry = tkinter.OptionMenu(self.mainWindow, self.charset, 'utf8', 'cp1251')
        self.charsetEntry.grid(row=2, column=1, sticky=tkinter.W)
        self.charset.set('utf8')

        pairLabel = tkinter.Label(self.mainWindow, text="Paired symbols")
        pairLabel.grid(row=3, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.pairEntry = tkinter.OptionMenu(self.mainWindow, self.pair, 'Remove', 'Ignore')
        self.pairEntry.grid(row=3, column=1, sticky=tkinter.W)
        self.pair.set('Remove')

        wordsLabel = tkinter.Label(self.mainWindow, text="Num of words")
        wordsLabel.grid(row=4, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.wordsEntry = tkinter.Spinbox(self.mainWindow, width=10, textvariable=self.words, from_=0, to=999999999999)
        self.wordsEntry.grid(row=4, column=1, sticky=tkinter.W)

        stemLabel = tkinter.Label(self.mainWindow, text="Use Stemming")
        stemLabel.grid(row=5, column=0, sticky=tkinter.E + tkinter.W + tkinter.N)
        self.stemButton = tkinter.Checkbutton(self.mainWindow, variable=self.stem)
        self.stemButton.grid(row=5, column=1, sticky=tkinter.W, columnspan=2)

        frame = tkinter.Frame(self.mainWindow);
        frame.grid(row=6, column=0, columnspan=3);

        self.start = tkinter.Button(frame, text="Start", width=13, command=self.startGen)
        self.start.grid(row=0, column=0)
        #self.stop = tkinter.Button(frame, text="Stop", width=13, command=self.stopGen, state=tkinter.DISABLED)
        #self.stop.grid(row=0, column=1)

        for i in range(0,3):
            self.mainWindow.columnconfigure(i, pad=5)
        for i in range(0, 6):
             self.mainWindow.rowconfigure(i, pad=5)

        self.mainWindow.mainloop()

    def setWidgetState(self, state):
        if state == tkinter.DISABLED:
            one, tow = tkinter.DISABLED, tkinter.NORMAL
        else:
            one, tow = tkinter.NORMAL, tkinter.DISABLED

        self.inputButton['state'] = one
        self.inputEntry['state'] = one
        self.outputButton['state'] = one
        self.outputEntry['state'] = one
        self.stemButton['state'] = one
        self.start['state'] = one
        #self.stop['state'] = tow

    def startGen(self):
        if self.input.get() == "":
            tkinter.messagebox.showerror('File not selected', 'Please select source file!', parent=self.mainWindow)
            return
        elif not os.path.exists(self.input.get()):
            tkinter.messagebox.showerror('File doesn\'t exist', 'Selected source file does not exist!', parent=self.mainWindow)
            return
        if self.output.get() == "":
            tkinter.messagebox.showerror('File not selected', 'Please select output file!', parent=self.mainWindow)
            return
        if self.words.get() <= 0:
            tkinter.messagebox.showerror('Invalid words count', 'Number of words to be generated must be grater than zero!', parent=self.mainWindow)
            return

        self.setWidgetState(tkinter.DISABLED)
        try:
            if self.oldInput != self.input.get() or self.stem.get() != self.oldStem or tkMessageBox.askyesno('Reload file?', 'You didn\'t change input file. However, should it be reloaded or use cached in RAM copy?\n Note: reloading will take a wile, depending of input file size.', parent=self.mainWindow):
                fp = codecs.open(self.input.get(), 'r', self.charset.get())
                self.Markov.load(unicode(fp.read()))
                fp.close()

            self.oldInput = self.input.get()
            self.oldStem = self.stem.get()

            self.Markov.useStemmer = self.stem.get()
            self.Markov.pair = self.pair.get()

            text = self.Markov.generate(self.words.get())

            fp = codecs.open(self.output.get(), 'w', self.charset.get())
            fp.write(text)
            fp.close()
        except UnicodeDecodeError:
            tkinter.messagebox.showerror('Charset error!', 'It seems you specified wrong input charset.', parent=self.mainWindow)

        self.setWidgetState(tkinter.NORMAL)

    def stopGen(self):
        self.setWidgetState(tkinter.NORMAL)

    def setInFile(self):
        self.input.set(tkinter.filedialog.askopenfilename(parent=self.mainWindow, title='Select source file'))

    def setOutFile(self):
        self.output.set(tkinter.filedialog.asksaveasfilename(defaultextension='.txt', parent=self.mainWindow, title='Select output file'))
GUI()
