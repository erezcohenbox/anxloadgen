import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output

class environmnt:
    def tempFileInfo():
        try:
            with open("temp", "r") as tempfile:
                tempFileValues = tempfile.read().split(',')
                tempfile.close()
            servers      = tempFileValues[0] # amount of servers
            usersValue   = tempFileValues[1] # total number of users
            startatValue = tempFileValues[2] # first user start at
            methodValue  = tempFileValues[3] # method
            return(servers, usersValue, startatValue, methodValue)
        except:
            return('error')

    def check(server, component, opration):
        host = configfile.sectionGetCredentials(server, component)[0]
        user = configfile.sectionGetCredentials(server, component)[1]
        password = configfile.sectionGetCredentials(server, component)[2]
        
        #remote_path = 'simulator/'
        remote_path = 'simulator/'
        local_path =  'scripts/' + str(environmnt.tempFileInfo()[1]) + '_users' + '_' + environmnt.tempFileInfo()[3] + '/server_'+ server
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_zip = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        
        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            transport = paramiko.Transport(host, 22)
            transport.connect(username=user,password=password)
            client.connect(hostname = host, username=user,password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
        except:
            return(False)

        # aeonix specific operations ##############################

        if opration in ["status"]:
            ssh_command ='sudo service aeonix status'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            running = response.count('running')
            stopped = response.count('stopped')
            return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error')            

        elif opration in ['version']:
            ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
            stdin,stdout,stderr = client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response if response !='' else 'error')

        # sipp specific operations ################################

        elif opration in ['jobs']:
            ssh_command = 'pgrep sipp'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            if response != '':
                return('running')
            elif response == '':
                return('stopped')

        elif opration in ['terminate']:
            ssh_command = 'killall sipp'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            ssh_command = 'cd ' + remote_path
            stdin,stdout,stderr = client.exec_command(ssh_command)
            ssh_command = 'echo ' + timestamp + ' terminate all running sipp jobs' + '\r >> ' + remote_path + 'load.info'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            return None

        elif opration in ['pack']:
            ssh_command = 'cd ' + remote_path + '; zip -r ../sim_`hostname`_' + timestamp_zip + '_logs.zip * &>/dev/null &'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            ssh_command = 'echo ' + timestamp + ' pack log files to zip' + '\r >> ' + remote_path + 'load.info'
            stdin,stdout,stderr = client.exec_command(ssh_command)

        elif opration in ['download']:
            ssh_command = 'cd ~'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            file_list = sftp.listdir()
            for item in file_list:
                if 'zip' in item:
                    print(item)
                    sftp.get(item, local_path + '/download/' + item)
                    ssh_command = 'echo ' + timestamp + ' download file: ' + item + '\r >> ' + remote_path + 'load.info'
                    stdin,stdout,stderr = client.exec_command(ssh_command)

        if opration in ['upload']:
            try:
                sftp.chdir(remote_path)
                #ssh_command = 'chmod +x *.sh'
                ssh_command = 'cd ' + remote_path + '; chmod +x *.sh' #anxd
                stdin,stdout,stderr = client.exec_command(ssh_command)
            except IOError:
                sftp.mkdir(remote_path)
                sftp.chdir(remote_path)
            
            files = os.listdir(local_path + '/sipp/')    
            for filename in files:
                sftp.put(local_path + '/sipp/' + filename, filename)
            ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; rm -rf *.zip'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            ssh_command = 'echo ' + timestamp + ' created and uploaded' + '\r >> ' + remote_path + 'load.info'
            stdin,stdout,stderr = client.exec_command(ssh_command)

        elif opration in ['clean']:
            ssh_command = 'cd ' + remote_path + '; chmod +x *.sh ; ./clean_logs.sh &>/dev/null &'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            ssh_command = 'echo ' + timestamp + ' clean up the log files ' + '\r >> ' + remote_path + 'load.info'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            return None

        elif opration in ['clean_zip']:
            ssh_command = 'cd ~' + '; rm -rf *.zip'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            #ssh_command = 'cd ' + remote_path + 'echo ' + timestamp + ' clean up the zip log files ' + '\r >> ' + remote_path + 'load.info'
            ssh_command = 'echo ' + timestamp + ' clean up the zip log files ' + '\r >> ' + remote_path + 'load.info'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            return None

        # common operations #######################################

        elif opration in ['hostname']:
            ssh_command = 'hostname'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response)

        elif opration in ['ipaddress']:
            ssh_command = 'hostname -I'
            stdin,stdout,stderr = client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response)