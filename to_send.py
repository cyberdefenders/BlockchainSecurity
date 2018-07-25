from OTXv2 import OTXv2
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
import getopt
import sys
from sendemail import sendemail

def tools():
    otx = OTXv2("e89676d6a1d9333168218175d7576abc24d33c0a1d20504e56a1151497146d14") # Initializes session with OTXv2 API using API key

    search = str(input('Please enter search: '))

    x = search.strip()


    pulses = otx.search_pulses(x, 40) # Retrieves list (in json format) of top 40 pulses with tag "crypto"

    pulsefile = open('pulseid.txt', "w+")

 # Loops through each individual pulse retrieved from OTX, and prints name & requested fields.
    '''
    pulls information from the results of the otx api
    writes to a txt file and checks to see if the threat
    has already been sent. By checking the pulseid in pulsesid
    '''
    with open('pulseid.txt', "r+") as pulsefile: # Reads text file pulse id 
            pulseIdList = pulsefile.read()  
    for singularPulse in pulses["results"]:
         
        name = singularPulse.get('name')
        description = singularPulse.get('description')
        modified = singularPulse.get('modified') 
        pulseid = singularPulse.get('id')
        if pulseid in pulseIdList:
            print("Threat has already been alerted")
        else:
            pulsefile = open('pulseid.txt', "a+")
            pulsefile.write(pulseid + "\n")
            pulsefile2 = open('email.txt', "a+")
            pulsefile2.write("Name: " +name+ "\n"+"\n" +"Description: " +description+ "\n"+"\n" +"Modified: " +modified+ "\n"+"\n"+"\n")  
    
    
    
    if pulseid not in pulseIdList:
        sendemail()
        open('email.txt', "w").close()
