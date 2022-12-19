import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output
#from selenium import webdriver
#from selenium.webdriver.edge import service
#from selenium.webdriver.edge.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#import pandas as pd
#pd.set_option('display.colheader_justify', 'right')


class prepare:

    def getUsersValue():
        sections = configfile.sectionsCount()
        users = {
            1: [1000, 2000, 3000, 5000],
            2: [2000, 4000, 6000, 8000],
            3: [3000, 6000, 9000, 12000],
            4: [4000, 8000, 10000, 12000],
            5: [5000, 10000, 15000, 20000],
            6: [6000, 12000, 18000, 24000]
        }
        default = users[sections][int(2)]
        print(bcolors.INFO + bcolors.IND + 'for ' + str(configfile.sectionsCount()) + ' server(s) configuration' + bcolors.RESET)
        print(bcolors.INFO + bcolors.IND + 'total amount of users options:' + bcolors.RESET)
        i = 0
        for element in users[sections]:
            i += 1
            print(bcolors.IND + str(i) + ': ' + str(element), end="  ")
        print()
        try:
            #choice = input()
            choice = input(bcolors.PROMPT + bcolors.IND + 'Choose [1-'+ str(i) + '] for total amount of users (default = option# 3): ' + bcolors.RESET)
            if int(choice) < 1 or int(choice) > i:
                return(False)
            selection = users[sections][int(choice) - 1]
            return(selection)
        except (ValueError, IndexError):
            return(default)


    def getStartatValue():
        startat =  [30000, 40000, 50000, 60000, 70000]
        default = startat[int(0)]
        print(bcolors.INFO + bcolors.IND + 'first user to begins at options :' + bcolors.RESET)
        i = 0
        for element in startat:
            i += 1
            print(bcolors.IND +str(i) + ': ' + str(element), end="  ")    
        print()    
        try:
            choice = input(bcolors.PROMPT + bcolors.IND + 'Choose [1-'+ str(i) + '] for first user (default = option# 1): ' + bcolors.RESET)
            if int(choice) < 1 or int(choice) > i:
                return(False)
            selection = startat[int(choice) - 1]
            return(selection)
        except (ValueError, IndexError):
            return(default)    
    
    def getMethodValue():
        method =  ['intra', 'inter', 'trunk']
        default = method[int(0)]
        print(bcolors.INFO + bcolors.IND + 'simulation method options:' + bcolors.RESET)
        i = 0
        for element in method:
            i += 1
            print(bcolors.IND + str(i) + ': ' + str(element), end="  ")    
        print()    
        try:
            choice = input(bcolors.PROMPT + bcolors.IND + 'Choose [1-'+ str(i) + '] for simulation method (default = option# 1): ' + bcolors.RESET)
            if int(choice) < 1 or int(choice) > i:
                return(False)
            selection = method[int(choice) - 1]
            return(selection)
        except (ValueError, IndexError):
            return(default)    

    def createSimFiles(usersValue, startatValue, methodValue):
        template_method = 'templates/'+ methodValue + '/'
        remote_path = 'simulator/'

        temp = [str(configfile.sectionsCount()), str(usersValue), str(startatValue), methodValue]
        with open("temp", "w") as tempfile:
            tempfile.writelines(",".join(temp))
            tempfile.close()
        
        shutil.rmtree('scripts/', ignore_errors=True)
        main_local_path = os.path.join ('scripts/', str(usersValue) + '_users'+ '_' + methodValue)
        os.makedirs(main_local_path, exist_ok = True)

        print()
        print(output.prompt_prepare_scripts_import_users_1 + str(usersValue) + output.prompt_prepare_scripts_import_users_2)
        print(output.prompt_prepare_scripts_import_users_3)

        with open(main_local_path +'/import_'+str(usersValue)+'_users.csv', 'w') as usersfile:
            for counter in range(startatValue, int(startatValue + usersValue)):
                usersfile.write(str(counter) +','+str(counter) +','+str(counter) +'_Desc,'+str(counter)+',SIP terminal'+',aeonix.com\n')
            usersfile.close()
        
        startatValueSplit = startatValue
        print()
        
        print(output.prompt_prepare_scripts_handling, end=" ")
        for section in configfile.sectionsNames():
            print(section, end=", ")
            sipp_local_path = os.path.join ('scripts/', str(usersValue) + '_users'+ '_' + methodValue + '/server_'+str(section) + '/sipp')
            aeonix_local_path = os.path.join ('scripts/', str(usersValue) + '_users'+ '_' + methodValue + '/server_'+str(section) + '/aeonix')
            download_local_path = os.path.join ('scripts/', str(usersValue) + '_users'+ '_' + methodValue + '/server_'+str(section) + '/download')
            os.makedirs(sipp_local_path, exist_ok = True)
            os.makedirs(aeonix_local_path, exist_ok = True)
            os.makedirs(download_local_path, exist_ok = True)

            #print(bcolors.INFO + '- copy all templates files to local /scripts directory..' + bcolors.RESET)
            shutil.copytree(template_method + '/sipp', sipp_local_path, dirs_exist_ok=True)
            shutil.copytree(template_method + '/aeonix', aeonix_local_path, dirs_exist_ok=True)

            #print(bcolors.INFO + '- parsing executable \'*.sh\' scripts' + bcolors.RESET)
            prepare.replace_string(sipp_local_path +'/register.sh','[servers]', configfile.sectionGetElement(section,'sipp_host') + ' ' + configfile.sectionGetElement(section,'aeonix_host'))
            prepare.replace_string(sipp_local_path +'/register.sh','[users]', str(int(usersValue/configfile.sectionsCount())))
            prepare.replace_string(sipp_local_path +'/answer.sh','[servers]', configfile.sectionGetElement(section,'sipp_host') + ' ' + configfile.sectionGetElement(section,'aeonix_host'))
            prepare.replace_string(sipp_local_path +'/call.sh','[servers]', configfile.sectionGetElement(section,'sipp_host') + ' ' + configfile.sectionGetElement(section,'aeonix_host'))
            prepare.replace_string(sipp_local_path +'/blf.sh','[servers]', configfile.sectionGetElement(section,'sipp_host') + ' ' + configfile.sectionGetElement(section,'aeonix_host'))

            #print(bcolors.INFO + '- creating sequantial \'*.csv\' files' + bcolors.RESET)
            with open(sipp_local_path +'/register.csv', 'w') as registerfile:
                registerfile.write('SEQUENTIAL\n')
                for counter in range(startatValueSplit, int(startatValueSplit + usersValue/configfile.sectionsCount())):
                    registerfile.write(str(counter) +';[authentication username='+str(counter) +' password=Aeonix123@]\n')
                registerfile.close()
            
            with open(sipp_local_path +'/call_answer.csv', 'w') as callanswerfile:
                callanswerfile.write('SEQUENTIAL\n')
                for counter in range(startatValueSplit, int(startatValueSplit + usersValue/configfile.sectionsCount()), 2):
                    callanswerfile.write(str(counter) + ';' + str(counter+1) +';\n')
                callanswerfile.close()

            #print(bcolors.INFO + '- creating \'load.info\' file' + bcolors.RESET)
            with open(sipp_local_path + '/load.info', 'w') as loadinfofile:
                loadinfofile.write(str(configfile.sectionsCount()) + ' aeonix server(s) simulation:\n ' + configfile.sectionsNamesDisplay() + '\n')
                loadinfofile.write('with total of ' + str(usersValue) + ' users ' + 'from user ' + str(startatValue) + 
                                    ' to user ' + str(startatValue + usersValue - 1) + '\n\n')
                loadinfofile.write('local simulation scope: ' + '\n')
                loadinfofile.write('sipp host ' + configfile.sectionGetElement(section,'sipp_host') + ' --> aeonix host ' + configfile.sectionGetElement(section,'aeonix_host')+ '\n')
                loadinfofile.write('from user ' + str(startatValueSplit) + ' to user ' + str(int(startatValueSplit + usersValue/configfile.sectionsCount() - 1)) + ' (' + str(int(usersValue/configfile.sectionsCount())) + ' users)\n\n')
                loadinfofile.close()
            shutil.copyfile(sipp_local_path + '/load.info', aeonix_local_path + '/load.info')

            #print(bcolors.INFO + '- setting \'cluster_disconnect.sh\' file' + bcolors.RESET)
            with open(aeonix_local_path + '/disconnect_server.sh', 'w', newline='\n') as disconnectfile:
                disconnectfile.write('#!/bin/sh\n\n')
                for server in configfile.sectionsNames():
                    if server == section:
                        continue
                    otherserver = configfile.sectionGetElement(server,'aeonix_host')
                    disconnectfile.write ('sudo iptables -A OUTPUT -d ' + otherserver + ' -j DROP\n')
                    disconnectfile.write ('sudo iptables -A INPUT -s ' + otherserver + ' -j DROP\n\n')
                    loadinfofile.close()
            
            startatValueSplit = startatValueSplit + int(usersValue/configfile.sectionsCount()) 


        #car = configfile.sectionsCount()
        #print(car)

        #car = configfile.sectionGetElement(section,'sipp_host') + ' ' + configfile.sectionGetElement(section,'aeonix_host')
        #a = configfile  .sectionGetElement(section,'sipp_host') + ' ' + 
        #print(car)

    def replace_string(filepath, replace, with_string):
        with open(filepath, 'r+') as f:
            replace_string = f.read().replace(replace, with_string)
        with open(filepath, 'w', newline='\n') as f:
            f.write(replace_string)
        f.close()