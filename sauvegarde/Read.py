#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import datetime
#from datetime import date
GPIO.setwarnings(False)
cmpt=0

date = datetime.datetime.now()
print(date)
    
continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
#print ("Press Ctrl-C to stop.")
#secteurBloc=eval(input("Entrez un Secteur :\n"))
secteurBlock2=12
#secteurBlock3=12

print ("Passer le tag RFID a lire")
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        # Print UID
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))
        # This is the default key for authentication
        keyA_Public = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Clee d authentification privée
        keyA_Privé = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
         
        key =  [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        #keyA_Privé = key
        #keyA_Public = key
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate with private key
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2,keyA_Privé, uid)
        # Check if authenticated
        if(status == MIFAREReader.MI_OK):
                next = False
                print ("Authentification Avec la Clee Privé ")
                print("\n")
                print("Carte deja initialisé_sur secteur ",secteurBlock2,"\n")
                print("INFORMATION Block: ")
                print ("Le secteur",secteurBlock2," contient actuellement : ")
                MIFAREReader.MFRC522_Read(secteurBlock2)
                print ("Le secteur",secteurBlock2+1," contient actuellement : ")
                MIFAREReader.MFRC522_Read(secteurBlock2+1)
                print ("Le secteur",secteurBlock2+2," contient actuellement : ")
                MIFAREReader.MFRC522_Read(secteurBlock2+2)
                # Stop
                #MIFAREReader.MFRC522_StopCrypto1()
                # Make sure to stop reading for cards
                continue_reading = False
                next = False
        else:
            print ("\nErreur d\'Authentification Avec la Clee Privé sur secteur ",secteurBlock2,"\n")
            next =True
            
        if(next == True):
            # Authenticate with Public  key
            status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2,keyA_Public, uid)
                # Check if authenticated
            if(status1 == MIFAREReader.MI_OK):
                print ("Authentification Avec la Clee Public sur secteur ",secteurBlock2,"\n")
                print ("Le secteur ",secteurBlock2+3,"contient actuellement :")
                MIFAREReader.MFRC522_Read(secteurBlock2+3)
                print ("Ecriture ...Clee Privé sur secteur",secteurBlock2+3)
                MIFAREReader.MFRC522_Write(secteurBlock2+3, data)
                print ("\n")
                print ("Carte initialisé sur Block",secteurBlock2+3)
                MIFAREReader.MFRC522_StopCrypto1()
                continue_reading = False
            else:
                print ("Error Authentification Avec la Clee Public sur secteur ",secteurBlock2)
                
