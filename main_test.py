import os, sys
from configfile import configfile
from prepare import *
from helpers import *
from environmnt import environmnt


#a = environmnt.check_aeonix('10.2.4.72', 'ipaddress')
#print(a)

#a = configfile.sectionGetCredentials('10.2.4.72', 'sipp')
#print(a[1])
#   def __init__(self, host, component, operation):
a = environmnt.check('10.2.4.72', 'sipp', 'upload')
print(a)

#car = configfile.sectionsNames()
#print(car)

#car = configfile.sectionsNames()[1]
#print(car)

#car = configfile.sectionsCount()
#print(car)

#car = configfile.sectionGetElement('10.10.10.10','sipp_user')
#print(car)

#---------------------------------------
#car = configfile.checkOptions()
#print(car)

#car = simfiles.setScope(2,1,0)
#print(car)

#print("Enter your choice [1-4]: ")
#users = simfiles.getUsersValue()
#print(users)

#print("Enter your choice [1-5]: ")
#startat = simfiles.getStartatValue()
#print(startat)

#print("Enter your choice [1-3]: ")
#method = simfiles.getMethodValue()
#print(method)


#car = configfile.initialize()
#print(car)

#car = configfile.sectionsNames()
#print(car)

#car = configfile.sectionsNamesDisplay()
#print(car)

#car = configfile.sectionsCount()
#print(car)

#car = configfile.sectionRemove('1.1.1.1')
#car = configfile.sectionGetElements('1.1.1.1')
#print(car)

#car = configfile.sectionAppend(['100.100.100.100','aeonixadmin1','anx1','aeonixweb1', 'anx2',
#                               '111.111.111.111','erezcohen3','tadirantele3'])



#car = configfile.sectionGetElement('1.1.1.1','sipp_user')
#print(car)
#car = configfile.sectionAdd()
#if car == False:
#    print('fail to update')
#else:
#    print(car)
#    configfile.sectionAppend(car)

#car = configfile.add('10.1.1.1', 'gg', 'ggg', '10.1.1.2', 'erezcohen', 'tadirantele')
#print(car)

#car = configfile.sectionsOverview()
#print(car)