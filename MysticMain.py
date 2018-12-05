import json
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar
from tkinter.filedialog import askopenfilename

Main_Menu = Tk(  )
Main_Menu.geometry("400x900")
Main_Menu.title("Mystic Project Format file wizard")
Main_Menu.iconbitmap('Mystic.ico')

#This is where we lauch the file manager bar.
def OpenFile():
    # Open Json fil format
    name = askopenfilename(initialdir="D:/Python/cobol/",
                           filetypes =(("Json file", "*.json"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'rb') as F:

            JsonData = json.load(F)
    except:
        print(format)
        print("No file exists")
    NameVarList = str("")
    for element in JsonData['fields']:
                #lstbox.insert(element['namevar'])
        print(element)
        print(element['namevar'])
        NameVarList = NameVarList + str(" ")  + str(element['namevar'])
        variables.set(NameVarList)
    scrollbar = Scrollbar(frame_Origine, orient=VERTICAL,command=lstbox.yview)

def select():
    reslist = list()
    selection = lstbox.curselection()
    VarListChoosen = str(" ")
    Choosen = StringVar()
    for i in selection:
        entree = lstbox.get(i)
        reslist.append(entree)

    for val in reslist:
        VarListChoosen = VarListChoosen + str(" ")  + val
        Choosen.set(VarListChoosen)
        #print(val)
    # create new list box with elements selected
    #-------------------------------------------
    lstbox2 = Listbox(frame_Destination, listvariable=Choosen,  width=40, height=10)
    lstbox2.grid(column=5, row=0, columnspan=1)

    btn_confirm = ttk.Button(frame_Origine, text="confirm", command=select)
    btn_confirm.grid(column=5, row=1)
    btn_confirm.grid_location(80,40)
    btn.config(state=DISABLED)



label = ttk.Label(Main_Menu, text ="Select fields from json file..",foreground="blue",font=("Helvetica", 16))
frame_Origine = ttk.Frame(Main_Menu, padding=(3, 3, 12, 12))
frame_Origine.grid(column=0, row=0, sticky=(N, S, E, W))
frame_Destination = ttk.Frame(Main_Menu, padding=(3, 3, 12, 12))
frame_Destination.grid(column=20, row=0, sticky=(N, S, E, W))
frame_Destination.grid_location(20,30)
variables = StringVar()
variables.set("\" Please select a file before\"")
btn = ttk.Button(frame_Origine, text="Validez", command=select)
btn.grid(column=1, row=1)

lstbox = Listbox(frame_Origine, listvariable=variables, selectmode=MULTIPLE, width=30, height=10)

lstbox.grid(column=0, row=0, columnspan=2)
#label.pack()

#Menu Bar

menu = Menu(Main_Menu)
Main_Menu.config(menu=menu)

file = Menu(menu)



file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())

menu.add_cascade(label = 'File', menu = file)
Main_Menu.mainloop()