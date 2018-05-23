#read2.py
#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.\n")
#secteurBlock = eval(input("Entrez un Secteur :\n"))
print ("Passer le tag RFID a lire\n")
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        continue_reading = False

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        keyA_Privé = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
        key = keyA_Privé

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        block=2
        secteurBlock = 8
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock, key, uid)
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            data_1 =MIFAREReader.MFRC522_Read(secteurBlock)
            print("data_1\n")
            print(str(chr(data_1[0])))
        else:
            print ("Authentication error on sector ",secteurBlock," block" ,block,"\n")
        
        block=3
        secteurBlock = 12
        print("\n")
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock, key, uid)
        if status == MIFAREReader.MI_OK:
            data_2 = MIFAREReader.MFRC522_Read(secteurBlock)
            print("data_2\n")
            print(str(chr(data_2[0])))
        else:
            print ("Authentication error on sector ",secteurBlock," block" ,block,"\n")
            
        
##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock+1, key, uid)
##
##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(secteurBlock+1)
##        else:
##            print ("Authentication error on sector ",secteurBlock+1," block ",block)
##
##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, secteurBlock+2, key, uid)
##
##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(3)
##            MIFAREReader.MFRC522_StopCrypto1()
##        else:
##            print ("Authentication error on sector ",secteurBlock+2," block ",block)