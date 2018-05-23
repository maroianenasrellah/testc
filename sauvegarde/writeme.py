#myprogram
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
#print(date)
continue_reading = True
encore = True
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

def cmpt():
    cmpt = cmpt + 1
    x = str(cmpt)
   # data.append(cmpt)
    if (len(data)<16):
            data.append(int(ord(x)))
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
secteurBlock2=8
secteurBlock3=12

INFO = my_function("Type-Datevalidité/CreditNbrseaux")
print ("Passer le tag RFID a lire\n")
sf=function()
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
# Scan for cards 
while continue_reading:
    # Scan for cards 
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
   # print("Scan for cards ...",status)
     # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
   # print("Get the UID ...",status)
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))
        # This is the default key for authentication
        keyA_Public = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # This is the Private key for authentication
        keyA_Privé = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2,  keyA_Privé, uid)
        if status == MIFAREReader.MI_OK:
            cmpt = cmpt+1
            buf = []
            buf.append(cmpt)
            print(cmpt)
                
            
            print("\nAuthentification Avec la Clee Privé sur secteur",secteurBlock2,"\n")
            print("Carte Déja initialisé sur secteur ",secteurBlock2+3,"\n")
            print ("Le secteur ",secteurBlock2," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock2)
            print ("mise a jour...La Date Limite de Validité sur secteur ",secteurBlock2,"\n")
            MIFAREReader.MFRC522_Write(secteurBlock2,INFO)
            print ("\n")
            print ("Le secteur ",secteurBlock2+1," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock2+1)
            print ("mise a jour...La Date Limite de Validité sur secteur ",secteurBlock2+1,"\n")
            MIFAREReader.MFRC522_Write(secteurBlock2+1,INFO)
##            print ("\n")
##            print ("Le secteur ",secteurBlock2+2," contient actuellement : ")
##            MIFAREReader.MFRC522_Read(secteurBlock2+2)
##            print ("mise a jour...La Date Limite de Validité sur secteur ",secteurBlock2+2,"\n")
##            MIFAREReader.MFRC522_Write(secteurBlock2+2,INFO)
            print ("\nLe secteur ",secteurBlock2+2," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock2+2)
            print ("mise a jour...sur secteur ",secteurBlock2+2,"\n")
            MIFAREReader.MFRC522_Write(secteurBlock2+2,w)
            MIFAREReader.MFRC522_Read(secteurBlock2+2)
            print("BLOC mis à jour : ")
            next = False
        else:
            print("\nAuthentification  error Avec la Clee Privé sur secteur",secteurBlock2,"\n")
            next =True
            
        if(next == True):
            status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock2, keyA_Public, uid)
            if(status1 == MIFAREReader.MI_OK):
                
                data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
                
                print ("Réussite Authentification Avec la Clee Public sur secteur ",secteurBlock2,"\n")
                print("Carte non-initialisé_sur secteur ",secteurBlock2,"\n")
                print ("Ecriture...Clee Privé sur Secteur",secteurBlock2+3)
                MIFAREReader.MFRC522_Write(secteurBlock2+3, data)
                print ("Le secteur ",secteurBlock2+3," contient actuellement : ")
                MIFAREReader.MFRC522_Read(secteurBlock2+3)
                print("Carte initialisé_sur secteur ",secteurBlock2,"\n")
            else:
                 print ("Erreur d\'Authentification Avec la Clee Public sur secteur",secteurBlock2)
                 continue_reading = False
####        # Authenticate
        status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock3,  keyA_Privé, uid)
        if status1 == MIFAREReader.MI_OK:
            print("Carte initialisé_sur secteur ",secteurBlock3,"\n")
            print("Authentication Avec la Clee Privé sur secteur",secteurBlock3,"\n")
             #secteur 
            print ("Le secteur ",secteurBlock3," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock3)
            print("mise à jour...La Date Dernier Passage  sur secteur",secteurBlock3)
            MIFAREReader.MFRC522_Write(secteurBlock3,sf)
            print ("Date Dernier Passage sur secteur: ",secteurBlock3)
            MIFAREReader.MFRC522_Read(secteurBlock3)
            #secteur 
            print ("Le secteur ",secteurBlock3+1," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock3+1)
            print("mise à jour...La Date Dernier Passage  sur secteur",secteurBlock3+1)
            MIFAREReader.MFRC522_Write(secteurBlock3+1,sf)
            print ("Date Dernier Passage sur secteur: ",secteurBlock3+1)
            MIFAREReader.MFRC522_Read(secteurBlock3+1)
             #secteur
            print ("Le secteur ",secteurBlock3+2," contient actuellement : ")
            MIFAREReader.MFRC522_Read(secteurBlock3+2)
            print("mise à jour...La Date Dernier Passage  sur secteur",secteurBlock3+2)
            MIFAREReader.MFRC522_Write(secteurBlock3+2,sf)
            print ("Date Dernier Passage sur secteur: ",secteurBlock3+2)
            MIFAREReader.MFRC522_Read(secteurBlock3+2)
            
            MIFAREReader.MFRC522_StopCrypto1()
            continue_reading = False
            nexto = False
        else:
            print("\nAuthentication error Avec la Clee Privé sur secteur",secteurBlock3,"\n")
            nexto =True
            
        if(nexto == True):
            status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock3, keyA_Public, uid)
            if(status1 == MIFAREReader.MI_OK):
                print ("Réussite Authentification Avec la Clee Public sur secteur ",secteurBlock3,"\n")
                print("Carte non initialisé_sur secteur ",secteurBlock3,"\n")
                print ("Le secteur ",secteurBlock3+3," contient actuellement : ")
                MIFAREReader.MFRC522_Read(secteurBlock3+3)
                print ("Ecriture...Clee Privé sur Secteur",secteurBlock3+3)
                MIFAREReader.MFRC522_Write(secteurBlock3+3, data)
                print ("Le secteur ",secteurBlock3+3," contient maintenant : ")
                MIFAREReader.MFRC522_Read(secteurBlock3+3)
                print("Carte initialisé_sur secteur ",secteurBlock3,"\n")
                MIFAREReader.MFRC522_StopCrypto1()
                continue_reading = False
            else:
                print ("Erreur d\'Authentification Avec la Clee Public sur secteur",secteurBlock3)
                continue_reading = False
        
