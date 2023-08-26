import subprocess
#only works on windows 10/11
import os




file= open('data.txt', 'a')
file.close()

def file_key_contents():
    keys=[]
    with open('data.txt', 'r') as data:
        data.read(8)
        line=data.readlines()
        key=[key.split('|')[1][1:-1] for key in line if ' ' in key]
    return key


def connect(profile, key):#TODO:
    try:
        interface="Wireless Network Connection"
        subprocess.run(['netsh', 'wlan', 'connect', profile, key, "WI-FI"])
    except:
        print("connection is already established")


def compare(list1=None, list2=file_key_contents()): 
    #comapres both list and only saves the elemnts not in list 2
    list3=[i for i in list1 if i not in list2]
    return list3


sub1= subprocess.check_output(["netsh", "wlan", "show", "profile"]).decode("utf-8").split("\n")
profiles=[i.split(":")[1][1:-1] for i in sub1 if "All User Profile" in i]
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
    if os.name == "nt":
        windows_wifi_grabber()
    else:
        print('invalid system')

if __name__ =="__main__":
    main()

