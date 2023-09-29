import subprocess
import os
import PySimpleGUI as sg 


file= open('data.txt', 'a')
file.close()


def file_key_contents():
    with open('data.txt', 'r') as data:
        data.read(8)
        line=data.readlines()
        key=[key.split('|')[1][1:-1] for key in line if ' ' in key]
    return key




def connect(profile, *argvs):#TODO:

    # Parameters:

    # Tag             Value
    # ssid          - SSID of the wireless network.
    # name          - Name of the profile to be used in connection attempt.
    # interface     - Name of the interface from which connection is attempted.
    try:
        
        subprocess.run(['netsh', 'wlan', 'connect', profile])
    except:
        print("connection is already established")


def compare(list1=None, list2=file_key_contents()): 
    #comapres both list and only saves the elemnts not in list 2
    list3=[i for i in list1 if i not in list2]
    return list3


sub1= subprocess.check_output(["netsh", "wlan", "show", "profile"]).decode("utf-8").split("\n")
profiles=[i.split(":")[1][1:-1] for i in sub1 if "All User Profile" in i]

def file_save_xml():
    for i in profiles:
        proc1 = subprocess.run(['netsh', 'wlan', 'export', 'profile', 'name='+i, 'key=clear', "folder=c:\\xml-files"])



def xml_import(drive, xmlfile=None):#TODO: test if it works
    if xmlfile==None:
        osfiles=os.listdir("c:\\xml-files")
        for xl in osfiles:
            proc= subprocess.run(['netsh', 'wlan', 'add', 'profile', drive+':\\xml-files\\'+xl])
    else:
        proc= subprocess.run(['netsh', 'wlan', 'add', 'profile', drive+':\\xml-files\\'+xmlfile])



def windows_wifi_grabber():
    with open("data.txt", "a") as data:

        for i in profiles:
            results= subprocess.check_output(["netsh", "wlan", "show", "profile", i, "key=clear"]).decode("utf-8").split("\n")
            re=[r.split(":")[1][1:-1]for r in results if "Key Content" in r]
            res= compare(re, list2=file_key_contents())
            if re not in res:


                try:

                    print("{:<30}|  {:<}".format(i, res[0]))
                    data.write('{:<30}| {:<}'.format(i, res[0])+'\n')

                except IndexError:
                    print("{:<30}|  {:<}".format(i, ""))

                except TypeError:
                    print("{:<30}| ".format(i))


        data.close()



def main():

#windows os = nt
#TODO:
#implement the same feaures for linux, Mac books and chrome os 

    osfiles=os.listdir("c:\\xml-files")
    sg.theme_background_color('DarkBlue')
    layout= [[sg.Button('Wifi Grabber')],
    [sg.Button('Display data')],          
    [sg.Text('', enable_events=True, key='GRAB')],
    [sg.Button('export')],
    [sg.Input("C")],
    [sg.Combo(osfiles)],
    [sg.Button('import')],
    [sg.Combo(profiles)],
    [sg.Button('Connect')]
    


    


    ]

    window= sg.Window('Wifi-Grabber', layout, size=(600, 500))

    running = True
    while running:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            running=False
        if event== 'Wifi Grabber':
            windows_wifi_grabber()
            window['GRAB'].update('Done')
        if event=='Display data':
            os.startfile("data.txt")
        if event== 'export':
            if os.path.exists('c:\\xml-files')==True:
                file_save_xml()
            elif os.path.exists('c:\\xml-files')==False:
                os.mkdir('c:\\xml-files')
                file_save_xml()
        if event=='import':
            #value[0] = chosen profile import
            xml_import(values[0], values[1])
            
        if event=='Connect':
            connect(values[2])

               



if __name__ == '__main__':
    main()


