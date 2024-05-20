import PySimpleGUI as pg
import numpy as np
from Guerison import *

# menu pour choisir l'option à traiter
menu = [['Fichier', ['New', 'Open', 'Save', 'Quit']],
            ['Options', ['Consultation', 'Cures', 'Symptoms', 'Effects']]]

# définition des layouts
layout_menu = [
    [pg.Menu(menu)],
]
# Layout à afficher pour l'ajout des médicaments
layout_meds = [
    [pg.Text("Welcome to the Aomin pharmacy \nEnter the list of medicaments")],
    [pg.Button("+",key="add_meds"),pg.Button("Save",key="-MEDS-")],   
    [pg.Button("x",key="del_med"),pg.Text("Curse name"),pg.Input(size=(20,15),key='-NAME0-'),pg.Text("Price(Ar)"),pg.Input(size=(20,15),key='-PRICE0-')]
]
# Layout à afficher pour l'ajout des symptômes
layout_sy = [
    [pg.Text("Enter the list of the symptoms in the input below separated with comma each other")],
    [pg.Input(key='-SYMP-')],
    [pg.Button("Add symptoms")]
]
# Layout pour afficher les effets de chaque médicaments sur chaque symptômes
layout_effects = []
# Layout pour afficher le degré de chaque symptôme 
layout_deg = []

col1 = pg.Column(layout_menu,visible=True,key="-MENU-")
col2 = pg.Column(layout_meds,visible=True,key="-CURE-")
col3 = pg.Column(layout_sy,visible=False,key="-SYM-")
col4 = pg.Column(layout_effects,visible=False,key="-EF-")
col5 = pg.Column(layout_deg,visible=False,key="-DEG-")

# définition de la layout principale
layout = [[col1,col2,col3,col4,col5]]

window = pg.Window("Aomin pharmacy",layout,size=(640,400),resizable=True)


def get_meds(values,nbreMeds):
    meds = {}
    for i in range(nbreMeds):
        name = values["-NAME"+str(i)+"-"]
        price = float(values["-PRICE"+str(i)+"-"])
        meds[name]= price
    return meds

def get_effect(values,medsName,symptomes):
    effects = {}
    for i in range(len(medsName)):
        effects[medsName[i]] = []
        for j in range(len(symptomes)):
            effects[medsName[i]].append(float(values[f"-{i}-{j}-"]))
    return effects

def get_degsympt(values,symptomes):
    sympt = {}
    for i in symptomes:
        sympt[i] = float(values[i])
    return sympt

def main():
    symptomes = []
    degSymptomes = {}
    medicaments = {}
    effects = {}
    nbreMeds = 1

    running = True 
    while running:
            event, values = window.read()
            print("event")
            print(event)
            if event == pg.WIN_CLOSED or event =="Escape:9" or event =="Quit":
                running = False
# layout symptoms
            elif event == "Symptoms":
                window["-SYM-"].update(visible=True)
                window["-CURE-"].update(visible=False)
                window["-EF-"].update(visible=False)
                window["-DEG-"].update(visible=False)

            elif event == "Add symptoms":
                symptomes = values["-SYMP-"].split(",")
                pg.popup("List symptoms added\nNow, enter the effects of the cures on the symptoms in Options > Effects")
                print(symptomes)
# layout cures
            elif event == "Cures":
                window["-SYM-"].update(visible=False)
                window["-CURE-"].update(visible=True)
                window["-EF-"].update(visible=False)
                window["-DEG-"].update(visible=False)
            elif event == "add_meds":
                window.extend_layout(window['-CURE-'],[[pg.Button("x",key="del_med"),pg.Text("Curse name"),pg.Input(size=(20,15),key=f"-NAME{nbreMeds}-"),
                pg.Text("Price(Ar)"),pg.Input(size=(20,15),key=f"-PRICE{nbreMeds}-")]])
                nbreMeds += 1
            elif event =="-MEDS-":
                medicaments = get_meds(values,nbreMeds)
                pg.popup("List medicaments added\nNow, enter the list of symptoms in Options > Symptoms")
                print(medicaments)
# layout effects
            elif event =="Effects":
                medsName = list(medicaments.keys())
                row0 = [[pg.Text("Effects of the cures on each known symptoms")] 
                        ,[pg.Text("",size=(10,1))]]
                for i in symptomes:
                    row0[1].append(pg.Text(i,size=(10,1)))
                window.extend_layout(window['-EF-'],row0)
                window["-EF-"].update(visible=True)
                window["-SYM-"].update(visible=False)
                window["-CURE-"].update(visible=False)
                window["-DEG-"].update(visible=False)
                rows = []
                for i in range(len(medsName)):
                    row = []
                    row.append(pg.Text(medsName[i],size=(10,1)))
                    for j in range(len(symptomes)):
                        row.append(pg.I(size=(10,1),key=f'-{i}-{j}-'))
                    rows.append(row)
                rows.append([pg.Button("Save",key="-EFFET-")])
                window.extend_layout(window['-EF-'],rows)
            
            elif event == "-EFFET-":
                medsName = list(medicaments.keys())
                effects  = get_effect(values,medsName,symptomes)
                pg.popup("List effect of the cures on each symptoms added\nNow, you can do the consultation in Options > Consultation")
                print(effects)
# layout pour récupérer le degré des symptômes
            elif event == "Consultation":
                rows = []
                rows.append([pg.Text("Hello, can you describe the degree of your symptoms below please by filling the blanks with numbers?")])
                for i in range(len(symptomes)):
                    row = []
                    row.append(pg.Text(symptomes[i],size=(10,1)))
                    row.append(pg.I(size=(10,1),key=f"{symptomes[i]}"))
                    rows.append(row)
                rows.append([pg.B("Treat",key="-TREAT-")])
                window.extend_layout(window["-DEG-"],rows)

                window["-EF-"].update(visible=False)
                window["-SYM-"].update(visible=False)
                window["-CURE-"].update(visible=False)
                window["-DEG-"].update(visible=True)
            elif event =="-TREAT-":
                degSymptomes = get_degsympt(values,symptomes)
                print(degSymptomes)
                message = get_minimal_price_cure(medicaments,degSymptomes,effects)
                window["-TREAT-"].update(visible=False)
                print("message")
                print(message)
                window.extend_layout(window["-DEG-"],[[pg.Text(message)]])
            else:
               pass

    window.close()

if __name__=="__main__":
    main()
