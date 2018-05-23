#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import os
import datetime
from datetime import date

GPIO.setwarnings(False) 
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()
    
def function():
    today = datetime.datetime.today()
    s="X"+today.strftime("%Y%m%d")
    data = []
    for c in  s:
        if (len(data)<16):
            data.append(int(ord(c)))
    while(len(data)!=16):
        data.append(0)
        
    return data

def my_function(kel_data):
    data = []
     #texte = input("Entrez une chaine de caractère :\n")
    texte = input("Entrez votre %s"%(kel_data)+" :\n")
    for c in texte:
        if (len(data)<16):
            data.append(int(ord(c)))
    while(len(data)!=16):
        data.append(0)
        
    return data
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
#secteurBloc=eval(input("Entrez un Secteur :\n"))
secteurBlock2=11
secteurBlock3=15

INFO = my_function("Type-Datevalidité/CreditNbrseaux")
print ("Placez votre carte RFID")
sf=function()
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Une carte est detectee
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Recuperation UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        #data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]

        # Print UID
        #print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))
    
        # This is the default key for authentication
        keyA_Public = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # This is the Private key for authentication
        keyA_Privé = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2,  keyA_Privé, uid)
        print ("\n")
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            print("Authentication Avec la Clee Privé sur secteur",secteurBlock2)
            print("Carte deja initialisé_sur secteur ",secteurBlock2,"\n")
            #secteur 8
            print ("Date Limite de Validite secteur 8: ")
            MIFAREReader.MFRC522_Read(8)
            print ("mise a jour...La Date sur secteur 8")
            MIFAREReader.MFRC522_Write(8,INFO)
            print ("\n")
            print ("secteur 8 contient maintenant : ")
            MIFAREReader.MFRC522_Read(8)
            #Le secteur 9
            print ("Date Limite de Validite secteur 9: ")
            MIFAREReader.MFRC522_Read(9)
            print ("mise a jour...La Date secteur 9")
            MIFAREReader.MFRC522_Write(9,INFO)
            print ("\n")
            print ("secteur 9 contient maintenant: ")
            MIFAREReader.MFRC522_Read(9)
            #Le secteur 10
            print ("Date Limite de Validite secteur 10: ")
            MIFAREReader.MFRC522_Read(10)
            print ("mise a jour...La Date secteur 10")
            MIFAREReader.MFRC522_Write(10,INFO)
            print ("\n")
            print ("secteur 10 contient maintenant : ")
            MIFAREReader.MFRC522_Read(10)
            
            data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
            
            print ("Ecriture ...sur Secteur",secteurBlock2)
            MIFAREReader.MFRC522_Write(secteurBlock2, data)
            print ("Le secteur",secteurBlock2," contient maintenant : ")
            MIFAREReader.MFRC522_Read(secteurBlock2)
            
           # (status,uid) = MIFAREReader.MFRC522_Anticoll()
            statussecteurBlock3 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock3,  keyA_Privé, uid)    
            if statussecteurBlock3 == MIFAREReader.MI_OK:
                print("Authentication Avec la Clee Privé sur secteur",secteurBlock3)
                print("Carte deja initialisé_sur secteur ",secteurBlock3,"\n")
                #secteur 12
                print("Le secteur 12 contient actuellement : ")
                MIFAREReader.MFRC522_Read(12)
                print("mise a jour...La Date sur secteur 12")
                MIFAREReader.MFRC522_Write(12,sf)
                print("\n")
                print("Date Dernier Passage : ")
                MIFAREReader.MFRC522_Read(12)
                #Le secteur 13
                print("Le secteur 13 contient actuellement: ")
                MIFAREReader.MFRC522_Read(13)
                print("mise a jour...La Date sur secteur 13")
                MIFAREReader.MFRC522_Write(13,sf)
                print("\n")
                print("Date Dernier Passage: ")
                MIFAREReader.MFRC522_Read(13)
                #Le secteur 14
                print("Le secteur 14 contient actuellement : ")
                MIFAREReader.MFRC522_Read(14)
                print ("mise a jour...La Date sur secteur 14")
                MIFAREReader.MFRC522_Write(14,sf)
                print("\n")
                print("secteur 14 contient maintenant : ")
                MIFAREReader.MFRC522_Read(14)
                
                MIFAREReader.MFRC522_StopCrypto1()
                # Make sure to stop reading for cards
                continue_reading = False
                nextsecteurBlock3 = False
            else:
                print ("Authentication error Avec la Clee Privé sur secteur",secteurBlock3)
                continue_reading = False
                nextsecteurBlock3 =True
                ######
            if(nextsecteurBlock3 == True):
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                MIFAREReader.MFRC522_SelectTag(uid)
                # Authenticate with Public  key
                status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock3,keyA_Public, uid)
                # Check if authenticated
                if(status1 == MIFAREReader.MI_OK):
                    data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
                    print ("Authentification Avec la Clee Public sur secteur ",secteurBlock3)
                    
                    print ("Le secteur ",secteurBlock3,"contient actuellement : ")
                    MIFAREReader.MFRC522_Read(secteurBlock3)
                    print ("Ecriture ...sur Secteur",secteurBlock3)
                    MIFAREReader.MFRC522_Write(secteurBlock3, data)
                    print ("Le secteur ",secteurBlock3,"contient maintenant : ")
                    MIFAREReader.MFRC522_Read(secteurBlock3)
                    print ("Carte initialisé secteur ",secteurBlock3,": ")
                    print("\n")
                    print ("Date Dernier Passage : ")
                    MIFAREReader.MFRC522_Read(12)
                    print ("mise a jour...La Date sur secteur 12")
                    MIFAREReader.MFRC522_Write(12,sf)
                    
                    MIFAREReader.MFRC522_StopCrypto1()
                    continue_reading = False
                    next = False
                else:
                    print ("Erreur d\'Authentification Avec la Clee Public sur secteur",secteurBlock3)        
        else:
            print ("Authentication error Avec la Clee Privé sur secteur",secteurBlock2)
            next =True
            
        if(next == True):
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                MIFAREReader.MFRC522_SelectTag(uid)
                # Authenticate with Public  key
                status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2,keyA_Public, uid)
                # Check if authenticated
                if(status1 == MIFAREReader.MI_OK):
                    data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
                    print ("Authentification Avec la Clee Public sur secteur ",secteurBlock2)
                    print ("Le secteur ",secteurBlock2,"contient actuellement : ")
                    MIFAREReader.MFRC522_Read(secteurBlock2)
                    print ("\n")           
                    print ("Ecriture ...sur Secteur",secteurBlock2)
                    MIFAREReader.MFRC522_Write(secteurBlock2, data)
                    print ("Le secteur ",secteurBlock2,"contient maintenant : ")
                    MIFAREReader.MFRC522_Read(secteurBlock2)
                    print ("\n")
                    print ("Carte initialisé secteur ",secteurBlock2,": ")
                    MIFAREReader.MFRC522_StopCrypto1()
                    continue_reading = False
                else:
                    print ("Erreur d\'Authentification Avec la Clee Public sur secteur",secteurBlock2)
                
##                status2 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 15,keyA_Public, uid)
##                if(status2 == MIFAREReader.MI_OK):
##                        print ("Le secteur 15 contient actuellement : ")
##                        MIFAREReader.MFRC522_Read(15)
##                        print("\n")
##                        print("Authentification Avec la Clee Public sur secteur 15")
##                else:
##                        print ("Erreur d\'Authentification Avec la Clee Public sur secteur 15")
##     
        #time.sleep(3)
