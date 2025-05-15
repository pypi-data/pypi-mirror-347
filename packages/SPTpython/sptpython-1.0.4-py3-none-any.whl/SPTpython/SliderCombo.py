import logging
logging.getLogger(__name__)

import tkinter

class SliderCombo(tkinter.Frame):
    """
    This class combines 5 tkinter widgets into one: a slider, an entry, a left and a right arrow (tkinter.Button instances),
    and a label. These all act as one entity with multiple ways to select a value. As the slider moves, the value
    in the entry box reflects the value of the slider. If the entry is modified, the slider moves to reflect that
    update.
    """
    def __init__(self, parent, title, lo, hi, init_val, background,type_):
        """
        Parameters
        ----------
        parent: tkinter parent widget
        title: title of slider
        lo: lower bound of slider
        hi: upper bound of slider
        init_val: initial position of slider (sets tkinter.Scale and initial value shown in tkinter.Entry)
        background: background color of slider
        type_: the type of the value in the slider. The user will only be able to put in information into the Entry
            box of this type.
        """
        self.background = background
        tkinter.Frame.__init__(self, parent)
        self.configure(background=self.background)
        self.val = tkinter.IntVar(self, value=init_val)
        self.val.trace('w', self.intVarCallback)
        self.command = None
        self.SVarModified = False
        self.type_ = type_

        self.slider = tkinter.Scale(self, from_=lo, to=hi, orient=tkinter.HORIZONTAL, command=self.sliderCallback,
                            background=self.background, showvalue=False, bd=0)
        self.slider.set(self.val.get())
        self.leftButton = tkinter.Button(self, text='<', command=self.makeArrowLambda(-1))
        self.rightButton = tkinter.Button(self, text='>', command=self.makeArrowLambda(1))
        self.SVar = tkinter.StringVar(self, value=str(self.val.get()))
        self.SVar.trace('w', self.SVarCallback)
        self.entry = tkinter.Entry(self, textvariable=self.SVar)
        self.entry.bind('<Return>', self.returnCallback)
        self.label = tkinter.Label(self, text=title, background=self.background, width=10)

        self.label.grid(row=0, column=0, sticky=tkinter.E)
        self.leftButton.grid(row=0, column=1)
        self.rightButton.grid(row=0, column=2)
        self.slider.grid(row=0, column=3, sticky=tkinter.EW)
        self.entry.grid(row=0, column=4, sticky=tkinter.W)

        self.columnconfigure(3, weight=1)
        self.runCommand = True

    def returnCallback(self, *_):
        """
        Gets run when the user hits Return while in the entry box
        """
        if self.SVarModified:
            val = int(self.SVar.get())
            self.SVarModified = False
            self.slider.set(val)
            self.val.set(val)

    def setCommand(self, command):
        """
        Sets command of the slider. Whenever the slider gets modified (after this is set), the command gets called.
        Parameters
        ----------
        command: command to be run on update of the slider

        Returns
        -------
        None
        """
        self.command = command

    def SVarCallback(self, *_):
        """
        Gets run whenever the value in the tkinter.Entry widget is modified
        """
        self.SVarModified = True

    def configureSlider(self, lo=None, hi=None):
        """
        Allows for redefinition of the lower and upper bounds of the slider
        Parameters
        ----------
        lo: new lower bound
        hi: new upper bound
        """
        if lo is not None:
            self.slider.configure(from_=lo)
        if hi is not None:
            self.slider.configure(to=hi)
        if lo is not None and hi is not None:
            val = self.val.get()
            if val < lo or val > hi:  # need to put the slider in the proper range
                self.slider.set(lo)
                self.SVar.set(lo)

    def arrowCallback(self, direction):
        """
        Gets called when the user clicks on one of the arrow buttons
        """
        val = self.val.get() + direction
        self.slider.set(val)
        self.SVar.set(str(val))
        self.val.set(val)

    def makeArrowLambda(self, direction):
        return lambda: self.arrowCallback(direction)

    def sliderCallback(self, _):
        """
        Gets run when the slider changes value. This changes the tkinter.IntVar associated with the tkinter.Scale instance,
        which will call self.intVarCallback()
        """
        val = int(self.slider.get())
        self.SVar.set(str(val))
        self.val.set(val)

    def intVarCallback(self, *_):
        """
        Gets called when the tkinter.Scale value changes. If self.command has been bound and has not been overridden
        with self.runCommand = False, run the command.
        """
        if self.command is not None and self.runCommand:
            self.command()

    def get_val(self):
        return self.val.get()

    def set_val(self, other, runCmd):
        """
        Modify the number on the slider
        Parameters
        ----------
        other: new value for the slider
        runCmd: boolean of whether to run the self.command callback

        Returns
        -------
        None
        """
        self.slider.set(other)
        self.SVar.set(str(other))
        if not runCmd:
            self.runCommand = False
        self.val.set(other)
        if not runCmd:
            self.runCommand = True
