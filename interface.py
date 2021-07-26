import PySimpleGUI as sg
import numpy as np
import sys

def FirstPage():
    sg.theme('DarkGreen')

    layout = [
        [sg.Text('A Novel Path Planning Optimization Algorithm for Semi-Autonomous UAVs in Bird Repellent Systems', size=(30, 2), font=("Georgia", 20))],
        [sg.Text('File name:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='fname', font=("Georgia", 11)), sg.Text('[Example: MissionOne]', size=(20, 0), font=("Georgia", 11))],
        [sg.Text('Output folder:', size=(15, 0), font=("Georgia", 11)), sg.Input(key='-IN3-', font=("Georgia", 11)), sg.FolderBrowse(target='-IN3-', font=("Georgia", 11))],
        [sg.Text('Number of PoIs:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='-POI-', font=("Georgia", 11))],
        [sg.Text('Mission velocity:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='velocity', font=("Georgia", 11)), sg.Text('[cm/s]', size=(20, 0), key = 'VUnit', font=("Georgia", 11))],
        [sg.Checkbox('Default velocity [500 cm/s]', default= False, key='VCheck', enable_events=True, font=("Georgia", 11))],
        [sg.Text('Flight time:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='ftime', font=("Georgia", 11)), sg.Text('[minutos]', size=(20, 0), font=("Georgia", 11))],
        [sg.Text('Random waypoints radius:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='Maxradius', font=("Georgia", 11)), sg.Text('[meters]', size=(20, 0), font=("Georgia", 11))],
        [sg.Text('Final error:', size=(15, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='Error', font=("Georgia", 11)),sg.Text('[percentage]', size=(20, 0), font=("Georgia", 11))],
        [sg.Text('Height:', size=(15, 0), font=("Georgia", 11)),sg.Input(size=(20, 0), key='height', font=("Georgia", 11)),sg.Text('[meters]', size=(20, 0), font=("Georgia", 11))],
        [sg.Button('Continue', font=("Georgia", 11)), sg.Button('Exit', font=("Georgia", 11))],
    ]
    return sg.Window('Software Interface', layout=layout, finalize=True)

def SecondPage():
    sg.theme('DarkGreen')

    layout = [
        [sg.Text('A Novel Path Planning Optimization Algorithm for Semi-Autonomous UAVs in Bird Repellent Systems', size=(30, 2), font=("Georgia", 20))],
        [sg.Text('', size=(15, 0), font=("Georgia", 11)), sg.Text('Latitude', size=(20, 0), font=("Georgia", 11)), sg.Text('Longitude', size=(10, 0), font=("Georgia", 11))],
        [sg.Text('Take-off:', size=(10, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='xtakeoff', font=("Georgia", 11)), sg.Input(size=(20, 0), key='ytakeoff', font=("Georgia", 11))],
        [sg.Text('Landing:', size=(10, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='xlanding', font=("Georgia", 11)), sg.Input(size=(20, 0), key='ylanding', font=("Georgia", 11))],
        [sg.Checkbox('Same take-off and landing', default=False, key='TLCheck', enable_events=True,font=("Georgia", 11))],
        [sg.Text('PoI:', size=(10, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='xPoI', font=("Georgia", 11)), sg.Input(size=(20, 0), key='yPoI', font=("Georgia", 11)), sg.Button('Ok', font=("Georgia", 11)), sg.Button('Clean', font=("Georgia", 11))],
        [sg.Text('Incidence Rate:', size=(10, 0), font=("Georgia", 11)), sg.Input(size=(20, 0), key='Per',visible=False, font=("Georgia", 11)), sg.Checkbox('Same Percentage', default=True, key='PCheck', enable_events=True,font=("Georgia", 11))],
        [sg.Text('Your PoI:', size=(10, 0), font=("Georgia", 11)), sg.Text(size=(20, 0), key='-xPoI-', font=("Georgia", 11)), sg.Text(size=(20, 0), key='-yPoI-', font=("Georgia", 11)),sg.Text(size=(20, 0), key='Rate', font=("Georgia", 11))],
        [sg.Button('Back', font=("Georgia", 11)), sg.Button('Start', font=("Georgia", 11)), sg.Button('Exit', font=("Georgia", 11))],
    ]
    return sg.Window('Software Interface', layout=layout, finalize=True)

def GraficInterface():
    winone, wintwo = FirstPage(), None

    it = 0
    while True:
        window, event, values = sg.read_all_windows()

        takeoff = [0,0]
        landing = [0,0]

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            sys.exit(0)

        if window == winone and event == 'Continue':
            wintwo = SecondPage()
            winone.hide()

            filename = values['fname']
            folder = values['-IN3-']
            ffolder = folder + '/' + filename + '.txt'

            nPOI = int(values['-POI-'])
            PointsofInterest = np.zeros((nPOI, 2))
            percentage = np.zeros(nPOI)

            if values['VCheck'] == True:
                velocity = int(500)
            elif values['VCheck'] == False:
                velocity = float(values['velocity'])

            vtime = float(values['ftime'])
            distance = int(velocity * vtime * 60 / 100)  # meter

            maxradius = int(values['Maxradius'])
            finalerror = distance*int(values['Error'])/100
            height = int(values['height'])

        if window == wintwo and event == 'Back':
            wintwo.hide()
            winone.un_hide()

        if window == wintwo and event == 'Start':
            takeoff[0] = float(values['xtakeoff'])
            takeoff[1] = float(values['ytakeoff'])
            if values['TLCheck'] == False:
                landing[0] = float(values['xlanding'])
                landing[1] = float(values['ylanding'])
            elif values['TLCheck'] == True:
                landing[0] = float(values['xtakeoff'])
                landing[1] = float(values['ytakeoff'])

            if values['PCheck'] == False:
                persum = np.sum(percentage)
                for i in range(nPOI):
                    percentage[i] = percentage[i]/persum
            window.close()
            break

        if window == wintwo and event == 'Ok' and it <= nPOI:

            PointsofInterest[it, 0] = float(values['xPoI'])
            PointsofInterest[it, 1] = float(values['yPoI'])

            window['-xPoI-'].update(PointsofInterest[it, 0])
            window['-yPoI-'].update(PointsofInterest[it, 1])

            if values['PCheck'] == True:
                wintwo['Per'].update(visible=False)
                wintwo['PCheck'].update(visible=False)
                percentage[it] = 1/nPOI
                window['Rate'].update(percentage[it])
            elif values['PCheck'] == False:
                wintwo['PCheck'].update(visible=False)
                percentage[it] = float(values['Per'])
                window['Rate'].update(float(values['Per']))

            it = it + 1
            if it == nPOI:
                window['-xPoI-'].update('All')
                window['-yPoI-'].update('All')
                window['Rate'].update('All')
                window['Ok'].update(visible=False)

        if window == window and event == 'Clean':
            it = 0
            window['Ok'].update(visible=True)
            window['-xPoI-'].update('')
            window['-yPoI-'].update('')
            window['Rate'].update('')

        if window == winone:
            if values['VCheck'] == True:
                winone['velocity'].update(visible=False)
                winone['VUnit'].update(visible=False)
            elif values['VCheck'] == False:
                winone['velocity'].update(visible=True)
                winone['VUnit'].update(visible=True)

        if window == wintwo:
            if values['PCheck'] == True:
                wintwo['Per'].update(visible=False)
            elif values['PCheck'] == False:
                wintwo['Per'].update(visible=True)

        if window == wintwo:
            if values['TLCheck'] == True:
                wintwo['xlanding'].update(visible=False)
                wintwo['ylanding'].update(visible=False)
            elif values['TLCheck'] == False:
                wintwo['xlanding'].update(visible=True)
                wintwo['ylanding'].update(visible=True)

    return takeoff, landing, PointsofInterest, percentage, distance, maxradius, finalerror, ffolder,height



