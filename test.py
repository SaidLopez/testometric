import PySimpleGUI as sg
import pandas as pd
import os

def read_files(files, thicknesses,location):
    
    dfs = []
    
    for i,file in enumerate(files):
        l= i+1
        data = pd.read_csv(f'{location}\{file}', sep = ',', header = None )
        data.columns = [f'Force (N) {l}',f'Deflection (mm) {l}',f'Time (s) {l}']
        data[f'Stress (MPA) {l}'] = data[f'Force (N) {l}'] / 550
        data[f'Thinkess (mm) {l}'] = thicknesses[i] - data[f'Deflection (mm) {l}']
        dfs.append(data)
    
    df = pd.concat(dfs, axis = 1)
    return df.to_csv(location + '\Wrapped data.csv')

sg.theme('Dark Blue 3')


### This is the original Layout to access everything in the tool ###

layout1 = [
    [sg.Text('Select a Directory (Only txt files outputted from the Testometric Kit)')],
    [sg.Input(size =(15,1)),sg.FolderBrowse(key="_FOLDER_")],
    [sg.OK(),sg.Cancel()]
]


layout2 = [
    [sg.Text('Input Gasket thicknesses',justification ='center', size=(50,1), font=['Comic Sans',15])],
    [sg.Frame('',[[sg.T('Thicknesses')]], key='-COL1-')],
    [sg.B("Create File", key = '-CSVFILE-')],
    [sg.Text('All done - Check the folder to see the final csv',key='_RESULT_', visible=False)]
    #Reused in the Google updates layout
    #[sg.Button(button_text="Back")]
]




layout = [
    [sg.Column(layout1, key='-MAIN-',element_justification = 'c'), 
     sg.Column(layout2, visible=False, key='_GASKETS_',element_justification = 'c')
    ]
    
]
# Create the window
window = sg.Window("Testometric data wrapper", layout, size = (800,500), element_justification = 'c')

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    elif event == 'OK':
        files_list = os.listdir(values['_FOLDER_'])
        window['-MAIN-'].update(visible=False)
        layout = '_GASKETS_'
        window[layout].update(visible=True)
        for i in range(len(files_list)):
            window.extend_layout(window['-COL1-'], [[sg.T(f'Gasket Thickness {i}'), sg.I(key=f'-IN-{i}-')]])
        
        
    elif event == '-CSVFILE-':
        gasket_thicknesses = [float(values[f'-IN-{i+1}-']) for i in range(len(files_list)) ]
        
        read_files(files_list,gasket_thicknesses, values['_FOLDER_'])
        window.Element('_RESULT_').update(visible = True)
    
           
window.close()